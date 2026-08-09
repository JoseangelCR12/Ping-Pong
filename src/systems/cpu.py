import math
import random
import config
from ..core.settings import data

class CPUBrain:
    has_hit_ball = False
    has_bounced = False  # Bandera para registrar el pique en el campo de la CPU
    toss_delay = 2.0 #La cpu tiene un delay antes de sacar
    prediction_done = False
    rebounded_on_table = False

    x_choice = None
    z_choice = None

    #Definimos la velocidad de movimiento de la cpu de acuerdo a la dificultad
    cpu_move_speed = config.CPU_MOVE_SPEED
    if data["cpu_level"] == 2:
        cpu_move_speed *= 0.6
    elif data["cpu_level"] == 1:
        cpu_move_speed *= 0.4

    @staticmethod
    def calculate_and_move(cpu_paddle, ball, table_limits, dt):
        """
        Cerebro de la IA con espera estricta de rebote:
        - Detecta cuándo la pelota toca la mesa de la CPU.
        - Mantiene la raqueta en posición de espera hasta que la pelota pica.
        - Solo tras el rebote inicia el swing y devuelve con fuerza controlada.
        """
        min_table_x, max_table_x, min_table_y, max_table_y, min_table_z, max_table_z = table_limits
        
        #si estamos en saque no calculamos nada aqui
        if CPUBrain.toss_delay < 2.0:
            return False

        # RESET DE ESTADO (Cuando la pelota vuelve al campo del jugador) 
        if ball.y <= config.NET_Y or ball.vy < -2.0:
            CPUBrain.has_hit_ball = False
            CPUBrain.has_bounced = False

        #  RETIRADA POST-GOLPE O PELOTA EN VIAJE AL JUGADOR 
        if CPUBrain.has_hit_ball or ball.vy < 0 or ball.y > config.OPPONENT_SIDE_Y:
            target_x = 0
            target_y = config.DEFAULT_CPU_CENTER_Y
            target_z = config.DEFAULT_CPU_CENTER_Z
            CPUBrain._smooth_move(cpu_paddle, target_x, target_y, target_z, dt, force_speed=CPUBrain.cpu_move_speed)
            CPUBrain.prediction_done = False
            return False


        if not CPUBrain.prediction_done and ball.y >= config.NET_Y:
            #  SIMULACIÓN DE TRAYECTORIA PRE-REBOTE 
            sim_x = ball.x
            sim_y = ball.y
            sim_z = ball.z
            sim_vx = ball.vx
            sim_vy = ball.vy
            sim_vz = ball.vz

            sim_dt = 1.0 / 60.0
            gravity_step = config.GRAVITY * sim_dt

            CPUBrain.rebounded_on_table = False

            # Buscamos el momento exacto en el que la pelota golpea la mesa
            while sim_vy > 0 and sim_y < config.OPPONENT_SIDE_Y and sim_z > max_table_z:
                sim_vx *= config.FRICTION
                sim_vy *= config.FRICTION
                sim_vz -= gravity_step

                sim_x += sim_vx * sim_dt
                sim_y += sim_vy * sim_dt
                sim_z += sim_vz * sim_dt

                # Detectamos si la pelota cruza el plano Z de la mesa (Z = min_table_z)
                if sim_z <= max_table_z:
                    if min_table_x <= sim_x <= max_table_x and config.NET_Y <= sim_y <= max_table_y:
                        CPUBrain.rebounded_on_table = True
                    break
            CPUBrain.prediction_done = True

        # Si no se detecta un rebote válido en la mesa, la pelota va fuera y nos apartamos
        if not CPUBrain.rebounded_on_table and CPUBrain.prediction_done and ball.vy != 0:
            target_x = max_table_x + 30 if ball.x < (min_table_x + max_table_x)/2 else min_table_x - 30
            target_y = config.DEFAULT_CPU_CENTER_Y
            target_z = config.DEFAULT_CPU_CENTER_Z
            CPUBrain._smooth_move(cpu_paddle, target_x, target_y, target_z,  dt, force_speed=CPUBrain.cpu_move_speed)
            return False


        paddle_depth = getattr(cpu_paddle, 'depth', 6.0)
        ball_radius = getattr(ball, 'radius', 5.0)

        # DETECCIÓN REAL DEL REBOTE EN EL LADO DE LA CPU 
        # Si la pelota está en el lado de la CPU (y > NET_Y) y...
        # Si la pelota está rozando la altura de la mesa (z <= min_table_z + ball_radius + 3.0)
        if ball.y > config.NET_Y:            
            if ball.z <= (max_table_z + ball_radius + 3.0) and ball.vz > 0:
                CPUBrain.has_bounced = True

        dist_x = abs(cpu_paddle.x - ball.x)
        dist_y = cpu_paddle.y - ball.y
        dist_z = abs(cpu_paddle.z - ball.z)

        # CONTACTO Y DEVOLUCIÓN (SOLO TRAS EL REBOTE) 
        step_y = max(8.0, ball.vy * dt)
        HIT_BOX_Y = paddle_depth + ball_radius + step_y + 4.0

        if CPUBrain.has_bounced and dist_y <= HIT_BOX_Y and dist_y >= -10.0 and dist_x < 50.0 and dist_z < 50.0:
            CPUBrain.has_hit_ball = True
            if data["cpu_level"] == 3:
                # Potencia calibrada 
                RETURN_POWER = max(480.0, min(600, abs(ball.vy) * 5))
                ball.vy = -RETURN_POWER

                # Dirección horizontal
                ball.vx = (-ball.x * 0.5 - ball.x) * 1.1

                # Parábola de retorno
                if ball.z > (max_table_z + 70.0):
                    if ball.y > config.OPPONENT_SIDE_Y - 50:
                        ball.vz = -50.0   # Remate mas largo si subió un poco y esta por el borde
                        ball.vy *= 1.5
                    elif ball.y <= config.NET_Y + 60:
                        ball.vz = -120.0   # Remate duro si esta cerca de la malla
                        ball.vy *= 1.3
                    else:
                        ball.vz = -60.0   # Remate si subió un poco
                        ball.vy *= 1.3
                elif ball.z > (max_table_z + 40.0):
                    if ball.y > config.OPPONENT_SIDE_Y - 60:
                        ball.vz = 30.0   # Remate mas largo si subió un poco y esta por el borde
                        ball.vy *= 1.5
                    elif ball.y <= config.NET_Y + 60:
                        ball.vz = -110.0   # Remate duro si esta cerca de la malla
                        ball.vy *= 1.2
                    else:
                        ball.vz = 20.0   # Remate si subió un poco
                        ball.vy *= 1.4
                else:
                    if ball.y <= config.NET_Y + 40:
                        ball.vz = -90.0   # Remate duro si esta cerca de la malla
                        ball.vy *= 1.2
                    else:
                        ball.vz = 90.0    # Arco para pasar la red
                    
                # Desacoplamiento físico
                ball.y = cpu_paddle.y - (paddle_depth + ball_radius + 6.0)
                return True
            
            elif data["cpu_level"] == 2:
                # Potencia calibrada 
                RETURN_POWER = max(370.0, min(500, abs(ball.vy) * 4))
                ball.vy = -RETURN_POWER

                # Dirección horizontal
                ball.vx = (-ball.x * 0.4 - ball.x) * 0.8

                # Parábola de retorno
                if ball.z > (max_table_z + 65.0):
                    if ball.y > config.OPPONENT_SIDE_Y - 60:
                        ball.vz = -10.0   # Remate mas largo si subió un poco y esta por el borde
                        ball.vy *= 1.5
                    elif ball.y < config.NET_Y + 60:
                        ball.vz = -90.0   # Remate duro si esta cerca de la malla
                        ball.vy *= 1.2
                    else:
                        ball.vz = -20.0   # Remate si subió un poco
                        ball.vy *= 1.5
                elif ball.z > (max_table_z + 40.0):
                    if ball.y > config.OPPONENT_SIDE_Y - 60:
                        ball.vz = 30.0   # golpe mas largo si subió un poco
                        ball.vy *= 1.3
                    else:
                        ball.vz = 20.0   # golpe si subió un poco
                        ball.vy *= 1.3    
                else:
                    ball.vz = 100.0    # Arco para pasar la red
                    
                # Desacoplamiento físico
                ball.y = cpu_paddle.y - (paddle_depth + ball_radius + 6.0)
                return True
            
            elif data["cpu_level"] == 1:
                # Potencia calibrada 
                RETURN_POWER = max(270.0, abs(ball.vy) * 2)
                ball.vy = -RETURN_POWER

                # Dirección horizontal
                ball.vx = (-ball.x * 0.3 - ball.x) * 0.6

                # Parábola de retorno
                if ball.z < (max_table_z + 30.0):
                    ball.vz = 80
                else:
                    ball.vz = 125.0    # Arco para pasar la red
               
                # Desacoplamiento físico
                ball.y = cpu_paddle.y - (paddle_depth + ball_radius + 6.0)
                return True

        # COMPORTAMIENTO DE ESPERA VS EMBESTIDA 
        target_x = ball.x
        target_z = max(max_table_z + ball_radius + 6.0, ball.z)

        if CPUBrain.has_bounced:
            # ¡Ya picó! La raqueta embiste hacia adelante para pegarle
            target_y = ball.y - 20.0
            EMBESTIDA_SPEED = max(CPUBrain.cpu_move_speed * 4.0, abs(ball.vy) * 2.5)
            if data["cpu_level"] == 2:
                EMBESTIDA_SPEED = max(CPUBrain.cpu_move_speed * 2.5, abs(ball.vy) * 1.2)
            elif data["cpu_level"] == 1:
                EMBESTIDA_SPEED = max(CPUBrain.cpu_move_speed * 1.5, abs(ball.vy))
        else:
            # Aún no pica: La raqueta espera pacientemente al fondo de su mesa
            target_y = config.OPPONENT_SIDE_Y + 40.0
            EMBESTIDA_SPEED = max(CPUBrain.cpu_move_speed * 1.2, abs(ball.vy))

        # Límites de seguridad
        NET_SAFETY_MARGIN_Y = 10.0
        min_cpu_y = config.NET_Y + NET_SAFETY_MARGIN_Y

        target_x = max(min_table_x - 10.0, min(target_x, max_table_x + 10.0))
        target_y = max(min_cpu_y, min(target_y, config.OPPONENT_SIDE_Y + 70.0))
        target_z = max(max_table_z + ball_radius + 6.0, min(target_z, config.MAX_PADDLE_Z))

        CPUBrain._smooth_move(cpu_paddle, target_x, target_y, target_z, dt, force_speed=EMBESTIDA_SPEED)

        return False

    @staticmethod
    def serve(cpu_paddle, ball, toss_function, dt):
        #La pelota se queda con la cpu y luego de un momento esta empieza el rally
            ball.x = cpu_paddle.x
            ball.y = cpu_paddle.y - 30
            ball.z = cpu_paddle.z

            #Le decimos a la cpu que no prediga mientras saca
            CPUBrain.prediction_done = True
            #Nos movemos a algun lado para sacar
            if CPUBrain.x_choice is None:
                CPUBrain.x_choice = random.choice([-100, 30, 78, 0, 20, -12]) #Posicion aleatoria en x al sacar
                CPUBrain.z_choice = random.choice([config.DEFAULT_CPU_CENTER_Z, 20, 60])
            target_x = CPUBrain.x_choice
            target_y = config.DEFAULT_CPU_CENTER_Y
            target_z = CPUBrain.z_choice 
            CPUBrain._smooth_move(cpu_paddle, target_x, target_y, target_z,  dt, force_speed=CPUBrain.cpu_move_speed)

            #va pasando el tiempo para que saque
            CPUBrain.toss_delay -= dt

            if CPUBrain.toss_delay <= 0.0 and toss_function():
                CPUBrain.toss_delay = 2.0
                CPUBrain.x_choice = None
                CPUBrain.z_choice = None

                #Se elige aleatoriamente una de 3 opciones
                choice = random.randrange(3)
                #La pelota se lanza al lado contrario picando una vez del lado de la cpu
                if data["cpu_level"] == 3:
                    if choice == 0:
                        ball.vx, ball.vy, ball.vz = 0, -300, -150
                    elif choice == 1:
                        ball.vx, ball.vy, ball.vz = -20, -450, -140
                    elif choice == 2:
                        ball.vx, ball.vy, ball.vz = 70, -300, -140
                elif data["cpu_level"] == 2:
                    if choice == 1:
                        ball.vx, ball.vy, ball.vz = 0, -230, -300
                    else:
                        ball.vx, ball.vy, ball.vz = -35, -240, -200
                elif data["cpu_level"] == 1:
                    ball.vx, ball.vy, ball.vz = 0, -240, -250
                                
                return True

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