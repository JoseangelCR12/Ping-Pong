import math
import config

class CPUBrain:
    @staticmethod
    def calculate_and_move(cpu_paddle, ball, table_limits, dt):
        """
        Cerebro matemático de la IA. Predice la física completa de la pelota,
        incluyendo el rebote en la mesa y la parábola ascendente posterior,
        para interceptarla en el aire de forma precisa.
        """
        min_table_x, max_table_x, min_table_y, max_table_y, min_table_z, _ = table_limits
        
        # Comportamiento de repliegue defensivo cuando la pelota se aleja hacia el jugador
        if ball.vy <= 0:
            target_x = config.DEFAULT_CPU_CENTER_X
            target_y = config.DEFAULT_CPU_CENTER_Y  
            target_z = config.DEFAULT_CPU_CENTER_Z
            CPUBrain._smooth_move(cpu_paddle, target_x, target_y, target_z, dt)
            return

        # --- SIMULACIÓN DE TRAYECTORIA PRE-REBOTE ---
        sim_x = ball.x
        sim_y = ball.y
        sim_z = ball.z
        sim_vx = ball.vx
        sim_vy = ball.vy
        sim_vz = ball.vz

        sim_dt = 1.0 / 60.0
        gravity_step = config.GRAVITY * sim_dt

        rebounded_on_table = False
        time_to_bounce = 0.0

        # Buscamos el momento exacto en el que la pelota golpea la mesa
        while sim_vy > 0 and sim_y < config.CPU_MAX_Y and sim_z > min_table_z:
            sim_vx *= config.FRICTION
            sim_vy *= config.FRICTION
            sim_vz -= gravity_step

            sim_x += sim_vx * sim_dt
            sim_y += sim_vy * sim_dt
            sim_z += sim_vz * sim_dt
            time_to_bounce += sim_dt

            # Detectamos si la pelota cruza el plano Z de la mesa (Z = min_table_z)
            if sim_z <= min_table_z:
                if min_table_x <= sim_x <= max_table_x and min_table_y <= sim_y <= max_table_y:
                    sim_z = min_table_z
                    sim_vz = -sim_vz * ball.restitution
                    rebounded_on_table = True
                break

        # --- EVALUACIÓN DE ESTRATEGIA ---
        # Si no se detecta un rebote válido en la mesa, la pelota va fuera y nos apartamos
        if not rebounded_on_table:
            target_x = max_table_x + 30 if sim_x < (min_table_x + max_table_x)/2 else min_table_x - 30
            target_y = config.DEFAULT_CPU_CENTER_Y
            target_z = config.DEFAULT_CPU_CENTER_Z
            CPUBrain._smooth_move(cpu_paddle, target_x, target_y, target_z, dt)
            return

        # --- SIMULACIÓN POST-REBOTE (INTERCEPCIÓN REAL) ---
        # Ahora que sabemos que rebotó, simulamos unos cuantos frames más hacia el futuro 
        # (por ejemplo, 10 frames tras el impacto) para buscarla en su fase ascendente ideal.
        frames_after_bounce = 10
        
        for _ in range(frames_after_bounce):
            sim_vx *= config.FRICTION
            sim_vy *= config.FRICTION
            sim_vz -= gravity_step

            sim_x += sim_vx * sim_dt
            sim_y += sim_vy * sim_dt
            sim_z += sim_vz * sim_dt

        # Las coordenadas de intercepción calculadas tras la parábola del rebote
        target_x = sim_x
        target_y = sim_y
        target_z = sim_z

        # Ajuste de las posiciones ideales dentro de los límites de movimiento de la CPU
        target_x = max(min_table_x - 10, min(target_x, max_table_x + 10))
        target_y = max(config.CPU_MIN_Y, min(target_y, config.CPU_MAX_Y))
        target_z = max(min_table_z + 10, min(target_z, config.MAX_PADDLE_Z)) # Asegurar altura de golpeo cómoda

        # pasamos el mov publico al paddle
        CPUBrain._smooth_move(cpu_paddle, target_x, target_y, target_z, dt)

    @staticmethod
    def _smooth_move(paddle, target_x, target_y, target_z, dt):
        """
        Interpola el movimiento en X, Y y Z usando la velocidad máxima de la CPU,
        lo que genera velocidades vx, vy, vz reales en la raqueta al desplazarse.
        """
        cpu_speed = config.CPU_MOVE_SPEED * dt

        if paddle.x < target_x:
            new_x = min(paddle.x + cpu_speed, target_x)
        elif paddle.x > target_x:
            new_x = max(paddle.x - cpu_speed, target_x)
        else:
            new_x = paddle.x

        if paddle.y < target_y:
            new_y = min(paddle.y + cpu_speed, target_y)
        elif paddle.y > target_y:
            new_y = max(paddle.y - cpu_speed, target_y)
        else:
            new_y = paddle.y

        if paddle.z < target_z:
            new_z = min(paddle.z + cpu_speed, target_z)
        elif paddle.z > target_z:
            new_z = max(paddle.z - cpu_speed, target_z)
        else:
            new_z = paddle.z

        # pasamos el mov publico al paddle
        paddle.update_pos(new_x, new_y, new_z, dt=dt)