import math
import config

class CPUBrain:
    has_hit_ball = False
    has_bounced = False  # Bandera para registrar el pique en el campo de la CPU

    @staticmethod
    def calculate_and_move(cpu_paddle, ball, table_limits, dt):
        """
        Cerebro de la IA con espera estricta de rebote:
        - Detecta cuándo la pelota toca la mesa de la CPU.
        - Mantiene la raqueta en posición de espera hasta que la pelota pica.
        - Solo tras el rebote inicia el swing y devuelve con fuerza controlada.
        """
        min_table_x, max_table_x, min_table_y, max_table_y, min_table_z, max_table_z = table_limits

        # --- 1. RESET DE ESTADO (Cuando la pelota vuelve al campo del jugador) ---
        if ball.y <= config.NET_Y or ball.vy < -20.0:
            CPUBrain.has_hit_ball = False
            CPUBrain.has_bounced = False

        # --- 2. RETIRADA POST-GOLPE O PELOTA EN VIAJE AL JUGADOR ---
        if CPUBrain.has_hit_ball or ball.vy <= 0:
            target_x = 0
            target_y = config.DEFAULT_CPU_CENTER_Y
            target_z = config.DEFAULT_CPU_CENTER_Z
            CPUBrain._smooth_move(cpu_paddle, target_x, target_y, target_z, dt, force_speed=config.CPU_MOVE_SPEED)
            return False

        paddle_depth = getattr(cpu_paddle, 'depth', 6.0)
        ball_radius = getattr(ball, 'radius', 5.0)

        # --- 3. DETECCIÓN REAL DEL REBOTE EN EL LADO DE LA CPU ---
        # Si la pelota está en el lado de la CPU (y > NET_Y) y...
        # Si la pelota está rozando la altura de la mesa (z <= min_table_z + ball_radius + 3.0)
        if ball.y > config.NET_Y:
            if ball.z <= (max_table_z + ball_radius + 3.0):
                CPUBrain.has_bounced = True

        dist_x = abs(cpu_paddle.x - ball.x)
        dist_y = cpu_paddle.y - ball.y
        dist_z = abs(cpu_paddle.z - ball.z)

        # --- 4. CONTACTO Y DEVOLUCIÓN (SOLO TRAS EL REBOTE) ---
        step_y = max(8.0, ball.vy * dt)
        HIT_BOX_Y = paddle_depth + ball_radius + step_y + 4.0

        if CPUBrain.has_bounced and dist_y <= HIT_BOX_Y and dist_y >= -10.0 and dist_x < 50.0 and dist_z < 50.0:
            CPUBrain.has_hit_ball = True

            # Potencia calibrada (entre 480 y 550)
            RETURN_POWER = max(480.0, abs(ball.vy) * 1.25)
            ball.vy = -RETURN_POWER

            # Dirección horizontal
            ball.vx = (-ball.x * 0.5 - ball.x) * 1.1

            # Parábola de retorno
            if ball.z > (min_table_z + 30.0):
                ball.vz = -50.0   # Remate suave si subió mucho
            else:
                ball.vz = 85.0    # Arco para pasar la red

            # Desacoplamiento físico
            ball.y = cpu_paddle.y - (paddle_depth + ball_radius + 6.0)
            return True

        # --- 5. COMPORTAMIENTO DE ESPERA VS EMBESTIDA ---
        target_x = ball.x
        target_z = max(min_table_z + ball_radius + 6.0, ball.z)

        if CPUBrain.has_bounced:
            # ¡Ya picó! La raqueta embiste hacia adelante para pegarle
            target_y = ball.y - 20.0
            EMBESTIDA_SPEED = max(config.CPU_MOVE_SPEED * 5.0, abs(ball.vy) * 3.0)
        else:
            # Aún no pica: La raqueta espera pacientemente al fondo de su mesa
            target_y = config.OPPONENT_SIDE_Y + 40.0
            EMBESTIDA_SPEED = max(config.CPU_MOVE_SPEED * 2.0, abs(ball.vy) * 1.2)

        # Límites de seguridad
        NET_SAFETY_MARGIN_Y = 10.0
        min_cpu_y = config.NET_Y + NET_SAFETY_MARGIN_Y

        target_x = max(min_table_x - 10.0, min(target_x, max_table_x + 10.0))
        target_y = max(min_cpu_y, min(target_y, config.OPPONENT_SIDE_Y + 70.0))
        target_z = max(min_table_z + ball_radius + 6.0, min(target_z, config.MAX_PADDLE_Z))

        CPUBrain._smooth_move(cpu_paddle, target_x, target_y, target_z, dt, force_speed=EMBESTIDA_SPEED)

        return False

    @staticmethod
    def _smooth_move(paddle, target_x, target_y, target_z, dt, force_speed):
        step = force_speed * dt

        if abs(target_x - paddle.x) <= step:
            new_x = target_x
        else:
            new_x = paddle.x + math.copysign(step, target_x - paddle.x)

        if abs(target_y - paddle.y) <= step:
            new_y = target_y
        else:
            new_y = paddle.y + math.copysign(step, target_y - paddle.y)

        if abs(target_z - paddle.z) <= step:
            new_z = target_z
        else:
            new_z = paddle.z + math.copysign(step, target_z - paddle.z)

        paddle.update_pos(new_x, new_y, new_z, dt=dt)