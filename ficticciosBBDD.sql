-- Primero, asegurarse de que las tablas estén vacías (opcional)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE reseñas_negocio;
TRUNCATE TABLE facturacion_suscripcion;
TRUNCATE TABLE citas;
TRUNCATE TABLE bloqueos_horario;
TRUNCATE TABLE horarios_negocio;
TRUNCATE TABLE servicios_negocio;
TRUNCATE TABLE empleados_negocio;
TRUNCATE TABLE negocios;
TRUNCATE TABLE categorias_negocio;
TRUNCATE TABLE usuarios;
TRUNCATE TABLE configuracion_plataforma;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. USUARIOS
INSERT INTO usuarios (
    id, username, email, first_name, last_name, password, is_active, is_staff, is_superuser,
    date_joined, last_login, tipo_usuario, genero, fecha_nacimiento, telefono, telefono_alternativo,
    direccion, ciudad, provincia, codigo_postal, pais, biografia, notificaciones_email,
    notificaciones_sms, notificaciones_push, idioma_preferido, zona_horaria, email_verificado,
    telefono_verificado, fecha_creacion, fecha_actualizacion, ultima_actividad
) VALUES 
-- Usuarios Admin/Staff
(UUID(), 'admin', 'admin@citalo.com', 'Administrador', 'Sistema', 'pbkdf2_sha256$600000$admin123', 1, 1, 1, NOW(), NOW(), 'admin', 'N', '1985-01-01', '+34600000000', '', 'Calle Admin 1', 'Madrid', 'Madrid', '28001', 'España', 'Administrador del sistema', 1, 0, 1, 'es', 'Europe/Madrid', 1, 1, NOW(), NOW(), NOW()),

-- Usuarios Propietarios de Negocio
(UUID(), 'maria_garcia', 'maria.garcia@email.com', 'María', 'García López', 'pbkdf2_sha256$600000$password123', 1, 0, 0, NOW(), NOW(), 'negocio', 'F', '1980-03-15', '+34612345678', '+34987654321', 'Avenida Belleza 25', 'Madrid', 'Madrid', '28010', 'España', 'Propietaria de salón de belleza con 15 años de experiencia', 1, 1, 1, 'es', 'Europe/Madrid', 1, 1, NOW(), NOW(), NOW()),

(UUID(), 'carlos_martinez', 'carlos.martinez@email.com', 'Carlos', 'Martínez Ruiz', 'pbkdf2_sha256$600000$password123', 1, 0, 0, NOW(), NOW(), 'negocio', 'M', '1975-07-22', '+34623456789', '', 'Calle Salud 42', 'Barcelona', 'Barcelona', '08001', 'España', 'Médico especialista en medicina general', 1, 0, 1, 'es', 'Europe/Madrid', 1, 1, NOW(), NOW(), NOW()),

(UUID(), 'ana_lopez', 'ana.lopez@email.com', 'Ana', 'López Fernández', 'pbkdf2_sha256$600000$password123', 1, 0, 0, NOW(), NOW(), 'negocio', 'F', '1982-11-08', '+34634567890', '', 'Plaza Motor 15', 'Valencia', 'Valencia', '46001', 'España', 'Mecánica automotriz especializada', 1, 1, 1, 'es', 'Europe/Madrid', 1, 1, NOW(), NOW(), NOW()),

-- Usuarios Empleados
(UUID(), 'lucia_torres', 'lucia.torres@email.com', 'Lucía', 'Torres Vega', 'pbkdf2_sha256$600000$password123', 1, 0, 0, NOW(), NOW(), 'empleado', 'F', '1990-05-12', '+34645678901', '', 'Calle Trabajo 8', 'Madrid', 'Madrid', '28015', 'España', 'Estilista profesional especializada en cortes modernos', 1, 1, 1, 'es', 'Europe/Madrid', 1, 1, NOW(), NOW(), NOW()),

(UUID(), 'pedro_sanchez', 'pedro.sanchez@email.com', 'Pedro', 'Sánchez Morales', 'pbkdf2_sha256$600000$password123', 1, 0, 0, NOW(), NOW(), 'empleado', 'M', '1988-09-30', '+34656789012', '', 'Avenida Medicina 20', 'Barcelona', 'Barcelona', '08015', 'España', 'Enfermero con experiencia en atención primaria', 1, 0, 1, 'es', 'Europe/Madrid', 1, 1, NOW(), NOW(), NOW()),

-- Usuarios Clientes
(UUID(), 'sofia_rodriguez', 'sofia.rodriguez@email.com', 'Sofía', 'Rodríguez Herrera', 'pbkdf2_sha256$600000$password123', 1, 0, 0, NOW(), NOW(), 'cliente', 'F', '1995-02-14', '+34667890123', '', 'Calle Cliente 33', 'Madrid', 'Madrid', '28020', 'España', 'Amante de los tratamientos de belleza y bienestar', 1, 1, 1, 'es', 'Europe/Madrid', 1, 1, NOW(), NOW(), NOW()),

(UUID(), 'david_fernandez', 'david.fernandez@email.com', 'David', 'Fernández Castro', 'pbkdf2_sha256$600000$password123', 1, 0, 0, NOW(), NOW(), 'cliente', 'M', '1987-12-03', '+34678901234', '', 'Plaza Principal 5', 'Barcelona', 'Barcelona', '08020', 'España', 'Profesional que valora la puntualidad y calidad', 1, 0, 1, 'es', 'Europe/Madrid', 1, 1, NOW(), NOW(), NOW()),

(UUID(), 'elena_gutierrez', 'elena.gutierrez@email.com', 'Elena', 'Gutiérrez Molina', 'pbkdf2_sha256$600000$password123', 1, 0, 0, NOW(), NOW(), 'cliente', 'F', '1992-06-18', '+34689012345', '', 'Avenida Nueva 77', 'Valencia', 'Valencia', '46020', 'España', 'Entusiasta del cuidado personal y wellness', 1, 1, 1, 'es', 'Europe/Madrid', 1, 1, NOW(), NOW(), NOW()),

(UUID(), 'miguel_jimenez', 'miguel.jimenez@email.com', 'Miguel', 'Jiménez Ruiz', 'pbkdf2_sha256$600000$password123', 1, 0, 0, NOW(), NOW(), 'cliente', 'M', '1985-08-25', '+34690123456', '', 'Calle Moderna 12', 'Sevilla', 'Sevilla', '41001', 'España', 'Cliente habitual de servicios de automoción', 1, 0, 1, 'es', 'Europe/Madrid', 1, 1, NOW(), NOW(), NOW());

-- 2. CATEGORÍAS DE NEGOCIO
INSERT INTO categorias_negocio (nombre, descripcion, icono, activa, orden, duracion_cita_default, permite_citas_online, requiere_confirmacion) VALUES
('Belleza y Estética', 'Salones de belleza, peluquerías, centros de estética y tratamientos de belleza', 'fas fa-cut', 1, 1, 45, 1, 0),
('Salud y Medicina', 'Consultas médicas, clínicas, centros de salud y especialistas médicos', 'fas fa-heartbeat', 1, 2, 30, 1, 1),
('Automoción', 'Talleres mecánicos, servicios de mantenimiento vehicular y reparaciones', 'fas fa-car', 1, 3, 60, 1, 1),
('Deportes y Fitness', 'Gimnasios, entrenadores personales, centros deportivos', 'fas fa-dumbbell', 1, 4, 60, 1, 0),
('Educación', 'Clases particulares, academias, cursos y formación', 'fas fa-graduation-cap', 1, 5, 60, 1, 0),
('Mascotas', 'Veterinarias, peluquerías caninas, cuidado de mascotas', 'fas fa-paw', 1, 6, 45, 1, 1);

-- 3. NEGOCIOS
INSERT INTO negocios (
    id, propietario_id, categoria_id, nombre, descripcion, slug, telefono, email, sitio_web,
    direccion, ciudad, provincia, codigo_postal, latitud, longitud, zona_horaria,
    tiempo_anticipacion_minimo, tiempo_cancelacion_limite, permite_reservas_multiples,
    estado_suscripcion, fecha_inicio_suscripcion, fecha_fin_suscripcion, calificacion_promedio,
    total_reseñas, activo, verificado, fecha_creacion, fecha_actualizacion
) VALUES
((SELECT UUID()), (SELECT id FROM usuarios WHERE username = 'maria_garcia'), (SELECT id FROM categorias_negocio WHERE nombre = 'Belleza y Estética'), 'Salón Belleza María', 'Salón de belleza integral con los mejores tratamientos de estética y peluquería. Especialistas en cortes modernos, coloración y tratamientos faciales.', 'salon-belleza-maria', '+34912345678', 'info@salonbellezamaria.com', 'https://www.salonbellezamaria.com', 'Avenida Belleza 25, Local 3', 'Madrid', 'Madrid', '28010', 40.4168, -3.7038, 'Europe/Madrid', 120, 240, 0, 'activa', DATE_SUB(NOW(), INTERVAL 30 DAY), DATE_ADD(NOW(), INTERVAL 335 DAY), 4.5, 15, 1, 1, NOW(), NOW()),

((SELECT UUID()), (SELECT id FROM usuarios WHERE username = 'carlos_martinez'), (SELECT id FROM categorias_negocio WHERE nombre = 'Salud y Medicina'), 'Clínica Dr. Martínez', 'Consulta médica especializada en medicina general y preventiva. Atención personalizada con cita previa.', 'clinica-dr-martinez', '+34934567890', 'consulta@drmartinez.com', 'https://www.clinicadrmartinez.com', 'Calle Salud 42, 2º Piso', 'Barcelona', 'Barcelona', '08001', 41.3851, 2.1734, 'Europe/Madrid', 60, 120, 1, 'activa', DATE_SUB(NOW(), INTERVAL 60 DAY), DATE_ADD(NOW(), INTERVAL 305 DAY), 4.8, 25, 1, 1, NOW(), NOW()),

((SELECT UUID()), (SELECT id FROM usuarios WHERE username = 'ana_lopez'), (SELECT id FROM categorias_negocio WHERE nombre = 'Automoción'), 'Taller Mecánico Ana', 'Taller especializado en reparación y mantenimiento de vehículos. Servicio rápido y garantizado.', 'taller-mecanico-ana', '+34963456789', 'contacto@tallerana.com', 'https://www.tallermecanico-ana.com', 'Plaza Motor 15, Nave 7', 'Valencia', 'Valencia', '46001', 39.4699, -0.3763, 'Europe/Madrid', 180, 360, 1, 'activa', DATE_SUB(NOW(), INTERVAL 15 DAY), DATE_ADD(NOW(), INTERVAL 350 DAY), 4.2, 8, 1, 1, NOW(), NOW());

-- 4. EMPLEADOS DE NEGOCIO
INSERT INTO empleados_negocio (
    usuario_id, negocio_id, tipo_empleado, especialidades, activo, fecha_incorporacion,
    puede_crear_citas, puede_modificar_citas, puede_cancelar_citas, puede_gestionar_horarios, puede_ver_estadisticas
) VALUES
((SELECT id FROM usuarios WHERE username = 'lucia_torres'), (SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), 'empleado', 'Cortes modernos, Coloración, Peinados para eventos', 1, DATE_SUB(NOW(), INTERVAL 180 DAY), 1, 1, 1, 0, 0),
((SELECT id FROM usuarios WHERE username = 'pedro_sanchez'), (SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 'empleado', 'Enfermería, Toma de constantes, Primeros auxilios', 1, DATE_SUB(NOW(), INTERVAL 90 DAY), 1, 1, 0, 0, 0);

-- 5. SERVICIOS DE NEGOCIO
INSERT INTO servicios_negocio (
    negocio_id, nombre, descripcion, duracion_minutos, precio, requiere_confirmacion,
    disponible_online, maximo_por_dia, orden, activo, fecha_creacion
) VALUES
-- Servicios Salón de Belleza
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), 'Corte de Cabello', 'Corte profesional adaptado a tu estilo y tipo de rostro', 45, 25.00, 0, 1, NULL, 1, 1, NOW()),
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), 'Coloración Completa', 'Tinte completo con productos de alta calidad', 120, 65.00, 1, 1, 3, 2, 1, NOW()),
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), 'Tratamiento Facial', 'Limpieza facial profunda con hidratación', 60, 40.00, 0, 1, 4, 3, 1, NOW()),
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), 'Peinado para Evento', 'Peinado profesional para ocasiones especiales', 90, 50.00, 1, 1, 2, 4, 1, NOW()),

-- Servicios Clínica Médica
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 'Consulta Medicina General', 'Consulta médica general con exploración completa', 30, 45.00, 1, 1, 20, 1, 1, NOW()),
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 'Revisión Médica Preventiva', 'Chequeo médico preventivo completo', 45, 60.00, 1, 1, 8, 2, 1, NOW()),
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 'Certificado Médico', 'Emisión de certificados médicos diversos', 15, 25.00, 0, 1, 15, 3, 1, NOW()),

-- Servicios Taller Mecánico
((SELECT id FROM negocios WHERE slug = 'taller-mecanico-ana'), 'Cambio de Aceite', 'Cambio de aceite y filtro con revisión básica', 30, 35.00, 0, 1, 8, 1, 1, NOW()),
((SELECT id FROM negocios WHERE slug = 'taller-mecanico-ana'), 'Revisión Pre-ITV', 'Revisión completa antes de pasar la ITV', 60, 75.00, 1, 1, 4, 2, 1, NOW()),
((SELECT id FROM negocios WHERE slug = 'taller-mecanico-ana'), 'Cambio de Neumáticos', 'Montaje y equilibrado de neumáticos', 45, 25.00, 0, 1, 6, 3, 1, NOW());

-- 6. HORARIOS DE NEGOCIO
INSERT INTO horarios_negocio (negocio_id, dia_semana, hora_inicio, hora_fin, activo) VALUES
-- Salón de Belleza (Lunes a Sábado)
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), 0, '09:00:00', '19:00:00', 1), -- Lunes
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), 1, '09:00:00', '19:00:00', 1), -- Martes
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), 2, '09:00:00', '19:00:00', 1), -- Miércoles
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), 3, '09:00:00', '19:00:00', 1), -- Jueves
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), 4, '09:00:00', '19:00:00', 1), -- Viernes
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), 5, '09:00:00', '14:00:00', 1), -- Sábado

-- Clínica (Lunes a Viernes)
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 0, '08:00:00', '14:00:00', 1), -- Lunes mañana
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 0, '16:00:00', '20:00:00', 1), -- Lunes tarde
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 1, '08:00:00', '14:00:00', 1), -- Martes mañana
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 1, '16:00:00', '20:00:00', 1), -- Martes tarde
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 2, '08:00:00', '14:00:00', 1), -- Miércoles mañana
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 2, '16:00:00', '20:00:00', 1), -- Miércoles tarde
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 3, '08:00:00', '14:00:00', 1), -- Jueves mañana
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 3, '16:00:00', '20:00:00', 1), -- Jueves tarde
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 4, '08:00:00', '14:00:00', 1), -- Viernes mañana

-- Taller Mecánico (Lunes a Viernes)
((SELECT id FROM negocios WHERE slug = 'taller-mecanico-ana'), 0, '08:00:00', '18:00:00', 1), -- Lunes
((SELECT id FROM negocios WHERE slug = 'taller-mecanico-ana'), 1, '08:00:00', '18:00:00', 1), -- Martes
((SELECT id FROM negocios WHERE slug = 'taller-mecanico-ana'), 2, '08:00:00', '18:00:00', 1), -- Miércoles
((SELECT id FROM negocios WHERE slug = 'taller-mecanico-ana'), 3, '08:00:00', '18:00:00', 1), -- Jueves
((SELECT id FROM negocios WHERE slug = 'taller-mecanico-ana'), 4, '08:00:00', '18:00:00', 1); -- Viernes

-- 7. CITAS
INSERT INTO citas (
    id, negocio_id, cliente_id, empleado_id, servicio_id, fecha_hora_inicio, fecha_hora_fin,
    estado, nombre_cliente, telefono_cliente, email_cliente, notas_cliente, precio_final,
    recordatorio_enviado, confirmacion_enviada, fecha_creacion, fecha_actualizacion
) VALUES
-- Citas para Salón de Belleza
((SELECT UUID()), (SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), (SELECT id FROM usuarios WHERE username = 'sofia_rodriguez'), (SELECT id FROM empleados_negocio WHERE usuario_id = (SELECT id FROM usuarios WHERE username = 'lucia_torres')), (SELECT id FROM servicios_negocio WHERE nombre = 'Corte de Cabello' AND negocio_id = (SELECT id FROM negocios WHERE slug = 'salon-belleza-maria')), '2024-10-15 10:00:00', '2024-10-15 10:45:00', 'completada', 'Sofía Rodríguez Herrera', '+34667890123', 'sofia.rodriguez@email.com', 'Me gustaría un corte moderno, no muy corto', 25.00, 1, 1, DATE_SUB(NOW(), INTERVAL 15 DAY), DATE_SUB(NOW(), INTERVAL 15 DAY)),

((SELECT UUID()), (SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), (SELECT id FROM usuarios WHERE username = 'elena_gutierrez'), (SELECT id FROM empleados_negocio WHERE usuario_id = (SELECT id FROM usuarios WHERE username = 'lucia_torres')), (SELECT id FROM servicios_negocio WHERE nombre = 'Tratamiento Facial' AND negocio_id = (SELECT id FROM negocios WHERE slug = 'salon-belleza-maria')), '2024-10-20 15:30:00', '2024-10-20 16:30:00', 'confirmada', 'Elena Gutiérrez Molina', '+34689012345', 'elena.gutierrez@email.com', 'Primera vez que vengo, tengo piel sensible', 40.00, 1, 1, DATE_SUB(NOW(), INTERVAL 10 DAY), DATE_SUB(NOW(), INTERVAL 10 DAY)),

-- Citas para Clínica Médica
((SELECT UUID()), (SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), (SELECT id FROM usuarios WHERE username = 'david_fernandez'), (SELECT id FROM empleados_negocio WHERE usuario_id = (SELECT id FROM usuarios WHERE username = 'pedro_sanchez')), (SELECT id FROM servicios_negocio WHERE nombre = 'Consulta Medicina General' AND negocio_id = (SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez')), '2024-10-18 09:00:00', '2024-10-18 09:30:00', 'completada', 'David Fernández Castro', '+34678901234', 'david.fernandez@email.com', 'Dolor de espalda desde hace una semana', 45.00, 1, 1, DATE_SUB(NOW(), INTERVAL 12 DAY), DATE_SUB(NOW(), INTERVAL 12 DAY)),

-- Citas para Taller Mecánico
((SELECT UUID()), (SELECT id FROM negocios WHERE slug = 'taller-mecanico-ana'), (SELECT id FROM usuarios WHERE username = 'miguel_jimenez'), NULL, (SELECT id FROM servicios_negocio WHERE nombre = 'Cambio de Aceite' AND negocio_id = (SELECT id FROM negocios WHERE slug = 'taller-mecanico-ana')), '2024-10-25 11:00:00', '2024-10-25 11:30:00', 'confirmada', 'Miguel Jiménez Ruiz', '+34690123456', 'miguel.jimenez@email.com', 'Seat León 2018, último cambio hace 6 meses', 35.00, 1, 1, DATE_SUB(NOW(), INTERVAL 5 DAY), DATE_SUB(NOW(), INTERVAL 5 DAY));

-- 8. RESEÑAS
INSERT INTO reseñas_negocio (
    negocio_id, cliente_id, cita_id, calificacion, comentario, calificacion_servicio,
    calificacion_atencion, calificacion_instalaciones, activa, fecha_creacion
) VALUES
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), (SELECT id FROM usuarios WHERE username = 'sofia_rodriguez'), (SELECT id FROM citas WHERE nombre_cliente = 'Sofía Rodríguez Herrera'), 5, 'Excelente servicio, Lucía es muy profesional y el resultado del corte superó mis expectativas. El salón está muy limpio y el ambiente es muy agradable.', 5, 5, 5, 1, DATE_SUB(NOW(), INTERVAL 14 DAY)),

((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), (SELECT id FROM usuarios WHERE username = 'david_fernandez'), (SELECT id FROM citas WHERE nombre_cliente = 'David Fernández Castro'), 5, 'El Dr. Martínez fue muy atento y profesional. Me explicó todo detalladamente y el tratamiento fue efectivo. Muy recomendable.', 5, 5, 4, 1, DATE_SUB(NOW(), INTERVAL 11 DAY));

-- 9. FACTURACIÓN
INSERT INTO facturacion_suscripcion (
    negocio_id, stripe_invoice_id, stripe_subscription_id, monto, moneda, periodo_inicio,
    periodo_fin, estado_pago, fecha_vencimiento, fecha_pago, numero_factura, fecha_creacion
) VALUES
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), 'in_1234567890', 'sub_1234567890', 29.99, 'EUR', '2024-09-01', '2024-09-30', 'pagado', '2024-09-15 23:59:59', '2024-09-14 10:30:00', 'FAC-2024-001', '2024-09-01 00:00:00'),

((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), 'in_0987654321', 'sub_0987654321', 49.99, 'EUR', '2024-09-01', '2024-09-30', 'pagado', '2024-09-15 23:59:59', '2024-09-13 14:20:00', 'FAC-2024-002', '2024-09-01 00:00:00'),

((SELECT id FROM negocios WHERE slug = 'taller-mecanico-ana'), 'in_1357924680', 'sub_1357924680', 29.99, 'EUR', '2024-09-15', '2024-10-14', 'pagado', '2024-09-30 23:59:59', '2024-09-29 16:45:00', 'FAC-2024-003', '2024-09-15 00:00:00');

-- 10. CONFIGURACIÓN DE PLATAFORMA
INSERT INTO configuracion_plataforma (clave, valor, descripcion, tipo_dato, activa, fecha_creacion) VALUES
('precio_suscripcion_basica', '29.99', 'Precio mensual de la suscripción básica en EUR', 'float', 1, NOW()),
('precio_suscripcion_premium', '49.99', 'Precio mensual de la suscripción premium en EUR', 'float', 1, NOW()),
('dias_prueba_gratuita', '14', 'Días de prueba gratuita para nuevos negocios', 'integer', 1, NOW()),
('max_citas_suscripcion_basica', '100', 'Máximo número de citas mensuales para suscripción básica', 'integer', 1, NOW()),
('max_citas_suscripcion_premium', '500', 'Máximo número de citas mensuales para suscripción premium', 'integer', 1, NOW()),
('email_soporte', 'soporte@citalo.com', 'Email de contacto para soporte técnico', 'string', 1, NOW()),
('telefono_soporte', '+34900123456', 'Teléfono de contacto para soporte', 'string', 1, NOW()),
('horario_soporte', '09:00-18:00', 'Horario de atención al cliente', 'string', 1, NOW()),
('stripe_public_key', 'pk_test_123456789', 'Clave pública de Stripe para pagos', 'string', 1, NOW()),
('google_maps_api_key', 'AIza123456789', 'Clave API de Google Maps', 'string', 1, NOW()),
('smtp_host', 'smtp.gmail.com', 'Servidor SMTP para envío de emails', 'string', 1, NOW()),
('smtp_port', '587', 'Puerto SMTP', 'integer', 1, NOW()),
('notificaciones_activas', 'true', 'Si las notificaciones están activas globalmente', 'boolean', 1, NOW()),
('mantenimiento_activo', 'false', 'Si la plataforma está en modo mantenimiento', 'boolean', 1, NOW()),
('version_app', '1.0.0', 'Versión actual de la aplicación', 'string', 1, NOW());

-- 11. BLOQUEOS DE HORARIO (Algunos ejemplos)
INSERT INTO bloqueos_horario (
    negocio_id, empleado_id, fecha_inicio, fecha_fin, tipo_bloqueo, motivo, activo, fecha_creacion
) VALUES
((SELECT id FROM negocios WHERE slug = 'salon-belleza-maria'), NULL, '2024-12-24 00:00:00', '2024-12-26 23:59:59', 'festivo', 'Vacaciones de Navidad', 1, NOW()),
((SELECT id FROM negocios WHERE slug = 'clinica-dr-martinez'), NULL, '2024-11-15 14:00:00', '2024-11-15 18:00:00', 'personal', 'Formación médica obligatoria', 1, NOW()),
((SELECT id FROM negocios WHERE slug = 'taller-mecanico-ana'), NULL, '2024-08-01 00:00:00', '2024-08-31 23:59:59', 'vacaciones', 'Vacaciones de verano', 1, NOW());

-- Consultas de verificación
SELECT 'RESUMEN DE DATOS INSERTADOS:' as '';
SELECT 'Usuarios creados:' as tipo, COUNT(*) as cantidad FROM usuarios
UNION ALL
SELECT 'Categorías creadas:', COUNT(*) FROM categorias_negocio
UNION ALL
SELECT 'Negocios creados:', COUNT(*) FROM negocios
UNION ALL
SELECT 'Empleados creados:', COUNT(*) FROM empleados_negocio
UNION ALL
SELECT 'Servicios creados:', COUNT(*) FROM servicios_negocio
UNION ALL
SELECT 'Horarios creados:', COUNT(*) FROM horarios_negocio
UNION ALL
SELECT 'Citas creadas:', COUNT(*) FROM citas
UNION ALL
SELECT 'Reseñas creadas:', COUNT(*) FROM reseñas_negocio
UNION ALL
SELECT 'Facturas creadas:', COUNT(*) FROM facturacion_suscripcion
UNION ALL
SELECT 'Configuraciones creadas:', COUNT(*) FROM configuracion_plataforma
UNION ALL
SELECT 'Bloqueos creados:', COUNT(*) FROM bloqueos_horario;