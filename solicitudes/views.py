from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render
from django.core.mail import send_mail, BadHeaderError
import os
from django.conf import settings
import threading  

def _ejecutar_envio_correo(asunto, mensaje, remitente, recipients):
    try:
        send_mail(
            asunto,
            mensaje,
            remitente,
            recipients,
            fail_silently=False,
        )
        return True
    except BadHeaderError as error:
        print(f'Error de encabezado de correo: {error}')
    except Exception as error:
        print(f'Error al enviar correo: {error}')
    return False

def enviar_correo(asunto, mensaje, destinatario):
    if not destinatario:
        return False

    if isinstance(destinatario, str):
        recipients = [destinatario]
    else:
        try:
            recipients = list(destinatario)
        except Exception:
            recipients = [str(destinatario)]

    remitente = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None)
    if not remitente:
        print('Email no enviado: no hay remitente configurado.')
        return False

    if not getattr(settings, 'EMAIL_ENABLED', False):
        print('ENV no configurado para enviar correos; omitiendo envío a', recipients)
        return False
    
    hilo = threading.Thread(
        target=_ejecutar_envio_correo,
        args=(asunto, mensaje, remitente, recipients)
    )
    hilo.start() 
    return True


def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM administradores
                WHERE usuario = %s
                  AND contraseña = %s
                """,
                [usuario, contraseña],
            )
            admin = cursor.fetchone()

        if admin:
            request.session['admin_id'] = admin[0]
            request.session['admin_role'] = admin[8] if len(admin) > 8 else ''
            return redirect('dashboard')

        messages.error(request, 'Usuario o contraseña incorrectos.')
        return redirect('login')

    return render(request, 'solicitudes/login_admin.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def index(request):
    return render(request, 'solicitudes/index.html')


def guardar(request):
    if request.method != 'POST':
        return redirect('index')

    nombre_solicitante = request.POST.get('nombre_solicitante')
    cedula_solicitante = request.POST.get('cedula_solicitante')
    telefono_solicitante = request.POST.get('telefono_solicitante')
    nombre_estudiante = request.POST.get('nombre_estudiante')
    seccion = request.POST.get('seccion')
    jornada = request.POST.get('jornada')
    nivel = request.POST.get('nivel')
    grado = request.POST.get('grado')
    paralelo = request.POST.get('paralelo')
    tecnica = request.POST.get('tecnica')
    paralelo_tecnico = request.POST.get('paralelo_tecnico')
    descripcion = request.POST.get('descripcion')
    correo_solicitante = request.POST.get('correo_solicitante')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*)
            FROM solicitudes
            WHERE cedula_solicitante = %s
            AND estado IN ('pendiente', 'en_proceso')
        """, [cedula_solicitante])

        existe = cursor.fetchone()[0]

        if existe > 0:
            messages.error(
                request,
                'Ya tiene una solicitud pendiente de atención. Debe esperar a que sea resuelta antes de registrar una nueva.'
            )
            return redirect('index')

    anexo_file = request.FILES.get('anexo')
    anexo_nombre = None

    if anexo_file:
        # CAMBIO AQUÍ: Ahora apuntamos directamente a settings.MEDIA_ROOT
        uploads_dir = settings.MEDIA_ROOT

        # Creamos la carpeta de media si no existe en el contenedor
        os.makedirs(uploads_dir, exist_ok=True)

        import uuid

        ext = os.path.splitext(anexo_file.name)[1]
        anexo_nombre = f"anexo_{uuid.uuid4()}{ext}"

        archivo_path = os.path.join(uploads_dir, anexo_nombre)

        # Guarda el archivo físicamente en la nueva carpeta persistente
        with open(archivo_path, 'wb+') as destination:
            for chunk in anexo_file.chunks():
                destination.write(chunk)

    with connection.cursor() as cursor:

        cursor.execute('SELECT MAX(id_solicitud) FROM solicitudes')
        row = cursor.fetchone()

        next_id = (row[0] or 0) + 1
        codigo = f"SOL-{next_id:04d}"

        cursor.execute(
            """
            INSERT INTO solicitudes (
                codigo,
                nombre_solicitante,
                cedula_solicitante,
                telefono_solicitante,
                nombre_estudiante,
                seccion,
                jornada,
                nivel,
                grado,
                paralelo,
                tecnica,
                paralelo_tecnico,
                descripcion,
                correo_solicitante,
                anexos,
                estado
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s,
                'pendiente'
            )
            """,
            [
                codigo,
                nombre_solicitante,
                cedula_solicitante,
                telefono_solicitante,
                nombre_estudiante,
                seccion,
                jornada,
                nivel,
                grado,
                paralelo,
                tecnica,
                paralelo_tecnico,
                descripcion,
                correo_solicitante,
                anexo_nombre,
            ],
        )

    if correo_solicitante:
        asunto = f"Solicitud {codigo} recibida"

        mensaje = (
            f"Estimado {nombre_solicitante},\n\n"
            f"Su solicitud {codigo} ha sido recibida.\n"
            "Su solicitud está en estado pendiente y se le notificará cualquier cambio.\n\n"
            "Gracias,\nUnidad Educativa Particular Técnica Cristiana Vida Nueva"
        )

        enviar_correo(
            asunto,
            mensaje,
            correo_solicitante
        )

    messages.success(
        request,
        'Solicitud enviada correctamente.'
    )

    return redirect('index')


def dashboard(request):
    role = request.session.get('admin_role')
    if role == 'superadmin':
        return redirect('dashboard_superadmin')
    if role == 'secretaria':
        return redirect('dashboard_secretaria')
    if role == 'docente':
        return redirect('dashboard_docente')
    return redirect('login')


def dashboard_secretaria(request):
    if request.session.get('admin_role') != 'secretaria':
        return redirect('login')

    admin_id = request.session.get('admin_id')
    nombre = ''
    solicitudes_pendientes = []

    q = request.GET.get('q', '').strip()
    curso = request.GET.get('curso', '').strip()
    paralelo = request.GET.get('paralelo', '').strip()
    fecha = request.GET.get('fecha', '').strip()

    with connection.cursor() as cursor:
        if admin_id:
            cursor.execute(
                "SELECT nombre, apellido FROM administradores WHERE id_admin = %s",
                [admin_id],
            )
            admin = cursor.fetchone()
            if admin:
                nombre = f"{admin[0]} {admin[1]}"

        cursor.execute("SELECT DISTINCT grado FROM solicitudes WHERE grado IS NOT NULL ORDER BY grado")
        grados = [r[0] for r in cursor.fetchall() if r[0] is not None]

        cursor.execute("SELECT DISTINCT paralelo FROM solicitudes WHERE paralelo IS NOT NULL ORDER BY paralelo")
        paralelos = [r[0] for r in cursor.fetchall() if r[0] is not None]

        sql = [
            "SELECT id_solicitud, codigo, nombre_solicitante, nombre_estudiante, seccion, jornada, nivel, grado, paralelo, fecha_creacion",
            "FROM solicitudes",
            "WHERE estado IN ('pendiente', 'recibido')",
        ]
        params = []

        if q:
            sql.append("AND (codigo LIKE %s OR nombre_solicitante LIKE %s OR nombre_estudiante LIKE %s)")
            likeq = f"%{q}%"
            params.extend([likeq, likeq, likeq])

        if curso:
            sql.append("AND grado = %s")
            params.append(curso)

        if paralelo:
            sql.append("AND paralelo = %s")
            params.append(paralelo)

        if fecha:
            sql.append("AND DATE(fecha_creacion) = %s")
            params.append(fecha)

        sql.append("ORDER BY fecha_creacion DESC")

        cursor.execute(" ".join(sql), params)
        solicitudes_pendientes = cursor.fetchall()

    return render(
        request,
        'solicitudes/dashboard_secretaria.html',
        {
            'nombre': nombre,
            'solicitudes_pendientes': solicitudes_pendientes,
            'grados': grados,
            'paralelos': paralelos,
            'filtro_q': q,
            'filtro_curso': curso,
            'filtro_paralelo': paralelo,
            'filtro_fecha': fecha,
        },
    )


def solicitudes_asignadas(request):
    if request.session.get('admin_role') != 'secretaria':
        return redirect('login')

    nombre = ''
    solicitudes = []

    q = request.GET.get('q', '').strip()
    curso = request.GET.get('curso', '').strip()
    paralelo = request.GET.get('paralelo', '').strip()
    fecha = request.GET.get('fecha', '').strip()

    with connection.cursor() as cursor:
        admin_id = request.session.get('admin_id')
        if admin_id:
            cursor.execute(
                "SELECT nombre, apellido FROM administradores WHERE id_admin = %s",
                [admin_id],
            )
            admin = cursor.fetchone()
            if admin:
                nombre = f"{admin[0]} {admin[1]}"

        cursor.execute("SELECT DISTINCT grado FROM solicitudes WHERE grado IS NOT NULL ORDER BY grado")
        grados = [r[0] for r in cursor.fetchall() if r[0] is not None]

        cursor.execute("SELECT DISTINCT paralelo FROM solicitudes WHERE paralelo IS NOT NULL ORDER BY paralelo")
        paralelos = [r[0] for r in cursor.fetchall() if r[0] is not None]

        sql = [
            "SELECT s.id_solicitud, s.codigo, s.nombre_solicitante, s.nombre_estudiante, s.seccion, s.jornada, s.nivel, s.grado, s.paralelo, CONCAT(a.nombre, ' ', a.apellido), s.fecha_actualizacion, s.fecha_creacion",
            "FROM solicitudes s",
            "LEFT JOIN administradores a ON a.id_admin = s.id_responsable",
            "WHERE s.estado IN ('asignada', 'resuelto', 'rechazado')",
        ]
        params = []

        if q:
            sql.append("AND (s.codigo LIKE %s OR s.nombre_solicitante LIKE %s OR s.nombre_estudiante LIKE %s)")
            likeq = f"%{q}%"
            params.extend([likeq, likeq, likeq])

        if curso:
            sql.append("AND s.grado = %s")
            params.append(curso)

        if paralelo:
            sql.append("AND s.paralelo = %s")
            params.append(paralelo)

        if fecha:
            sql.append("AND DATE(s.fecha_creacion) = %s")
            params.append(fecha)

        sql.append("ORDER BY s.fecha_actualizacion DESC")

        cursor.execute(" ".join(sql), params)
        solicitudes = cursor.fetchall()

    return render(
        request,
        'solicitudes/solicitudes_asignadas.html',
        {
            'nombre': nombre,
            'solicitudes_asignadas': solicitudes,
            'grados': grados,
            'paralelos': paralelos,
            'filtro_q': q,
            'filtro_curso': curso,
            'filtro_paralelo': paralelo,
            'filtro_fecha': fecha,
        },
    )
def solicitud_detalle(request, solicitud_id):
    if request.session.get('admin_role') != 'secretaria':
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM solicitudes WHERE id_solicitud = %s",
            [solicitud_id],
        )
        solicitud = cursor.fetchone()

        if not solicitud:
            return redirect('dashboard_secretaria')

        # Asumimos que el estado está en la columna índice 12 (basado en tu estructura)
        estado_actual = solicitud[12]

        cursor.execute(
            "SELECT id_admin, nombre, apellido FROM administradores WHERE rol = 'docente'",
        )
        docentes = cursor.fetchall()

        if request.method == 'POST':
            # --- BLOQUEO DE EDICIÓN ---
            if estado_actual == 'resuelto':
                messages.error(request, "Error: No se puede modificar una solicitud que ya está resuelta.")
                return redirect('dashboard_secretaria')

            id_responsable = request.POST.get('id_responsable')
            respuesta = request.POST.get('respuesta')
            estado = 'asignada' if id_responsable else 'pendiente'

            cursor.execute(
                "SELECT correo_solicitante, codigo FROM solicitudes WHERE id_solicitud = %s",
                [solicitud_id],
            )
            correo_row = cursor.fetchone()
            correo_solicitante = correo_row[0] if correo_row else None
            codigo = correo_row[1] if correo_row else ''

            docente_nombre = ''
            if id_responsable:
                cursor.execute(
                    "SELECT nombre, apellido FROM administradores WHERE id_admin = %s",
                    [id_responsable],
                )
                docente = cursor.fetchone()
                if docente:
                    docente_nombre = f"{docente[0]} {docente[1]}"

            cursor.execute(
                """
                UPDATE solicitudes
                SET id_responsable = %s,
                    respuesta = %s,
                    estado = %s,
                    fecha_actualizacion = NOW()
                WHERE id_solicitud = %s
                """,
                [id_responsable or None, respuesta, estado, solicitud_id],
            )

            if correo_solicitante:
                asunto = f"Solicitud {codigo} actualizada"
                mensaje = (
                    "Estimado,\n\n"
                    f"Su solicitud {codigo} ha sido actualizada por Secretaría.\n"
                    f"Estado: {estado}.\n"
                )
                if docente_nombre:
                    mensaje += f"Se ha asignado al docente {docente_nombre}.\n"
                if respuesta:
                    mensaje += f"Respuesta: {respuesta}.\n"
                mensaje += "\nGracias,\nUnidad Educativa Particular Técnica Cristiana Vida Nueva"
                
                enviar_correo(asunto, mensaje, correo_solicitante)

            messages.success(request, "Los cambios de la solicitud se guardaron con éxito.")
            return redirect('dashboard_secretaria')

    return render(
        request,
        'solicitudes/solicitud_detalle.html',
        {
            'solicitud': solicitud,
            'docentes': docentes,
        },
    )

def dashboard_docente(request):
    if request.session.get('admin_role') != 'docente':
        return redirect('login')

    admin_id = request.session.get('admin_id')
    nombre_completo = ''
    solicitudes_activas = []
    solicitudes_finalizadas = []
    pendientes = 0
    proceso = 0
    resueltas = 0

    with connection.cursor() as cursor:
        if admin_id:
            cursor.execute(
                "SELECT nombre, apellido FROM administradores WHERE id_admin = %s",
                [admin_id],
            )
            admin = cursor.fetchone()
            if admin:
                nombre_completo = f"{admin[0]} {admin[1]}"

        cursor.execute(
            "SELECT COUNT(*) FROM solicitudes WHERE id_responsable = %s AND estado = 'asignada'",
            [admin_id],
        )
        pendientes = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM solicitudes WHERE id_responsable = %s AND estado = 'en_proceso'",
            [admin_id],
        )
        proceso = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM solicitudes WHERE id_responsable = %s AND estado = 'resuelto'",
            [admin_id],
        )
        resueltas = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT
                id_solicitud,
                codigo,
                nombre_estudiante,
                nombre_solicitante,
                grado,
                paralelo,
                fecha_creacion,
                estado
            FROM solicitudes
            WHERE id_responsable = %s
            AND estado IN ('asignada', 'en_proceso')
            ORDER BY fecha_creacion DESC
            """,
            [admin_id],
        )
        solicitudes_activas = cursor.fetchall()

        cursor.execute(
            """
            SELECT
                codigo,
                nombre_estudiante,
                grado,
                paralelo,
                estado,
                fecha_actualizacion
            FROM solicitudes
            WHERE id_responsable = %s
            AND estado IN ('resuelto', 'rechazado')
            ORDER BY fecha_actualizacion DESC
            """,
            [admin_id],
        )
        solicitudes_finalizadas = cursor.fetchall()

    total_asignadas = pendientes + proceso + resueltas

    return render(
        request,
        'solicitudes/dashboard_docente.html',
        {
            'nombre_completo': nombre_completo,
            'pendientes': pendientes,
            'proceso': proceso,
            'resueltas': resueltas,
            'total_asignadas': total_asignadas,
            'solicitudes_activas': solicitudes_activas,
            'solicitudes_finalizadas': solicitudes_finalizadas,
        },
    )


def docente_detalle(request, solicitud_id):
    if request.session.get('admin_role') != 'docente':
        return redirect('login')

    admin_id = request.session.get('admin_id')
    nombre_completo = ''
    solicitud = None

    with connection.cursor() as cursor:
        if admin_id:
            cursor.execute(
                "SELECT nombre, apellido FROM administradores WHERE id_admin = %s",
                [admin_id],
            )
            admin = cursor.fetchone()
            if admin:
                nombre_completo = f"{admin[0]} {admin[1]}"

        cursor.execute(
            "SELECT * FROM solicitudes WHERE id_solicitud = %s AND id_responsable = %s",
            [solicitud_id, admin_id],
        )
        solicitud = cursor.fetchone()

        if not solicitud:
            return redirect('dashboard_docente')

        if request.method == 'POST':
            estado = request.POST.get('estado')
            respuesta = request.POST.get('respuesta')

            cursor.execute(
                "SELECT correo_solicitante, codigo FROM solicitudes WHERE id_solicitud = %s",
                [solicitud_id],
            )
            correo_row = cursor.fetchone()
            correo_solicitante = correo_row[0] if correo_row else None
            codigo = correo_row[1] if correo_row else ''

            cursor.execute(
                """
                UPDATE solicitudes
                SET estado = %s,
                    respuesta = %s,
                    fecha_actualizacion = NOW()
                WHERE id_solicitud = %s
                """,
                [estado, respuesta, solicitud_id],
            )

            if correo_solicitante:
                asunto = f"Estado actualizado para su solicitud {codigo}"
                mensaje = (
                    f"Estimado {solicitud[2]},\n\n"
                    f"El estado de su solicitud {codigo} ha sido cambiado a {estado}.\n"
                )
                if respuesta:
                    mensaje += f"Respuesta: {respuesta}.\n"
                mensaje += "\nGracias,\nUnidad Educativa Particlar Técnica Cristiana Vida Nueva"
            
                enviar_correo(asunto, mensaje, correo_solicitante)

            messages.success(request, 'Solicitud actualizada correctamente.')
            return redirect('dashboard_docente')

    estado_css = ''
    if solicitud and solicitud[12]:
        estado_css = solicitud[12].lower().replace(' ', '_')

    return render(
        request,
        'solicitudes/docente_detalle.html',
        {
            'nombre_completo': nombre_completo,
            'solicitud': solicitud,
            'estado_css': estado_css,
        },
    )


def dashboard_superadmin(request):
    if request.session.get('admin_role') != 'superadmin':
        return redirect('login')

    nombre = ''
    admins = []
    total_admins = 0
    total_docentes = 0
    total_secretarias = 0
    total_superadmins = 0

    with connection.cursor() as cursor:
        admin_id = request.session.get('admin_id')
        if admin_id:
            cursor.execute(
                "SELECT nombre, apellido FROM administradores WHERE id_admin = %s",
                [admin_id],
            )
            admin = cursor.fetchone()
            if admin:
                nombre = f"{admin[0]} {admin[1]}"

        cursor.execute(
            "SELECT COUNT(*) FROM administradores"
        )
        total_admins = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM administradores WHERE rol = 'docente'"
        )
        total_docentes = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM administradores WHERE rol = 'secretaria'"
        )
        total_secretarias = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM administradores WHERE rol = 'superadmin'"
        )
        total_superadmins = cursor.fetchone()[0]

        cursor.execute(
            "SELECT id_admin, usuario, CONCAT(nombre, ' ', apellido) AS nombre_completo, correo, rol, telefono"
             " FROM administradores"
        )
        admins = cursor.fetchall()

    return render(
        request,
        'solicitudes/dashboard_superadmin.html',
        {
            'nombre': nombre,
            'admins': admins,
            'total_admins': total_admins,
            'total_docentes': total_docentes,
            'total_secretarias': total_secretarias,
            'total_superadmins': total_superadmins,
        },
    )


import re

def registro_admin(request):
    if request.session.get('admin_role') != 'superadmin':
        return redirect('login')

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        cedula = request.POST.get('cedula', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        correo = request.POST.get('correo', '').strip()
        usuario = request.POST.get('usuario', '').strip()
        contraseña = request.POST.get('contraseña', '').strip()
        rol = request.POST.get('rol')

        # Validar nombre
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre):
            messages.error(request, 'El nombre solo puede contener letras.')
            return redirect('registro_admin')

        # Validar apellido
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', apellido):
            messages.error(request, 'El apellido solo puede contener letras.')
            return redirect('registro_admin')

        # Validar cédula
        if not cedula.isdigit():
            messages.error(request, 'La cédula solo puede contener números.')
            return redirect('registro_admin')

        if len(cedula) != 10:
            messages.error(request, 'La cédula debe tener 10 dígitos.')
            return redirect('registro_admin')

        # Validar teléfono
        if not telefono.isdigit():
            messages.error(request, 'El teléfono solo puede contener números.')
            return redirect('registro_admin')

        if len(telefono) != 10:
            messages.error(request, 'El teléfono debe tener 10 dígitos.')
            return redirect('registro_admin')

        # Validar correo
        if '@' not in correo:
            messages.error(request, 'Correo electrónico inválido.')
            return redirect('registro_admin')

        # Validar usuario
        if len(usuario) < 4:
            messages.error(request, 'El usuario debe tener al menos 4 caracteres.')
            return redirect('registro_admin')

        # Validar contraseña
        if len(contraseña) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return redirect('registro_admin')

        with connection.cursor() as cursor:

            # Verificar usuario repetido
            cursor.execute(
                "SELECT COUNT(*) FROM administradores WHERE usuario = %s",
                [usuario]
            )

            if cursor.fetchone()[0] > 0:
                messages.error(request, 'El nombre de usuario ya existe.')
                return redirect('registro_admin')

            # Verificar cédula repetida
            cursor.execute(
                "SELECT COUNT(*) FROM administradores WHERE cedula = %s",
                [cedula]
            )

            if cursor.fetchone()[0] > 0:
                messages.error(request, 'Ya existe un usuario registrado con esa cédula.')
                return redirect('registro_admin')

            cursor.execute(
                """
                INSERT INTO administradores (
                    nombre,
                    apellido,
                    cedula,
                    telefono,
                    correo,
                    usuario,
                    contraseña,
                    rol
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    nombre,
                    apellido,
                    cedula,
                    telefono,
                    correo,
                    usuario,
                    contraseña,
                    rol,
                ],
            )

        messages.success(request, 'Administrador registrado correctamente.')
        return redirect('dashboard_superadmin')

    return render(request, 'solicitudes/registro_admin.html')

def editar_usuario(request, admin_id):
    if request.session.get('admin_role') != 'superadmin':
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id_admin, nombre, apellido, cedula, telefono, correo, usuario, rol
            FROM administradores
            WHERE id_admin = %s
            """,
            [admin_id],
        )
        admin = cursor.fetchone()

    if not admin:
        return redirect('dashboard_superadmin')

    return render(request, 'solicitudes/editar_usuario.html', {'admin': admin})


def actualizar_usuario(request, admin_id):
    if request.session.get('admin_role') != 'superadmin':
        return redirect('login')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        rol = request.POST.get('rol')

        with connection.cursor() as cursor:

            if contraseña:

                cursor.execute(
                    """
                    UPDATE administradores
                    SET nombre = %s,
                        apellido = %s,
                        cedula = %s,
                        telefono = %s,
                        correo = %s,
                        usuario = %s,
                        contraseña = %s,
                        rol = %s
                    WHERE id_admin = %s
                    """,
                    [
                        nombre,
                        apellido,
                        cedula,
                        telefono,
                        correo,
                        usuario,
                        contraseña,
                        rol,
                        admin_id
                    ],
                )

            else:

                cursor.execute(
                    """
                    UPDATE administradores
                    SET nombre = %s,
                        apellido = %s,
                        cedula = %s,
                        telefono = %s,
                        correo = %s,
                        usuario = %s,
                        rol = %s
                    WHERE id_admin = %s
                    """,
                    [
                        nombre,
                        apellido,
                        cedula,
                        telefono,
                        correo,
                        usuario,
                        rol,
                        admin_id
                    ],
                )

        messages.success(
            request,
            'Usuario actualizado correctamente.'
        )

    return redirect('dashboard_superadmin')


def eliminar_usuario(request, admin_id):
    if request.session.get('admin_role') != 'superadmin':
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM administradores WHERE id_admin = %s",
            [admin_id],
        )
    messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('dashboard_superadmin')


def error_404(request, exception):
    return render(request, 'solicitudes/error.html', status=404)

def error_500(request):
    return render(request, 'solicitudes/error.html', status=500)


def error_403(request, exception=None):
    return render(
        request,
        'solicitudes/error.html',
        {
            'status_code': 403,
            'error_title': 'Acceso denegado'
        },
        status=403
    )
def eliminar_solicitud(request, solicitud_id):
    if request.session.get('admin_role') != 'secretaria':
        return redirect('login')

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT codigo, correo_solicitante 
                FROM solicitudes 
                WHERE id_solicitud = %s
            """, [solicitud_id])
            solicitud_data = cursor.fetchone()
            cursor.execute("SELECT anexos FROM solicitudes WHERE id_solicitud = %s", [solicitud_id])
            row = cursor.fetchone()
            if row and row[0]:
                archivo_path = os.path.join(settings.BASE_DIR, 'solicitudes', 'static', 'uploads', row[0])
                if os.path.exists(archivo_path):
                    os.remove(archivo_path)
            cursor.execute("DELETE FROM solicitudes WHERE id_solicitud = %s", [solicitud_id])
        if solicitud_data:
            codigo_sol_texto = solicitud_data[0]
            correo_destinatario = solicitud_data[1]

            asunto_correo = f"Notificación de Estado: Solicitud {codigo_sol_texto} - UE Vida Nueva"
            
            mensaje_cuerpo = (
                f"Estimado(a) Estudiante.\n\n"
                f"Te informamos que tu solicitud con código {codigo_sol_texto} ha sido revisada por el departamento administrativo.\n\n"
                "Lamentablemente, la solicitud NO HA SIDO ASIGNADA y ha sido dada de baja del sistema debido a "
                "incoherencias detectadas en la información proporcionada o en la documentación adjunta.\n\n"
                "Por favor, acércate a la secretaría del plantel o vuelve a ingresar la solicitud a través del sistema, "
                "verificando minuciosamente que todos los campos y documentos cargados sean correctos.\n\n"
                "Atentamente,\n"
                "Departamento de Secretaría\n"
                "Unidad Educativa Particular Técnica Cristiana 'Vida Nueva'"
            )
            enviar_correo(asunto_correo, mensaje_cuerpo, correo_destinatario)
        messages.success(request, "La solicitud fue eliminada permanentemente y se notificó al estudiante por correo electrónico.")
        return redirect('dashboard_secretaria')

    return redirect('dashboard_secretaria')