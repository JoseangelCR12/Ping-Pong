import config
import math

class Physics:
    
    @staticmethod
    def move_ball(ball, dt):
        """Actualiza la posición de la pelota aplicando gravedad y fricción"""
        Physics._apply_gravity(ball, dt)
        Physics._apply_friction(ball)
        Physics._update_ball_position(ball, dt)

    @staticmethod
    def _apply_gravity(ball, dt):
        """Aplica la gravedad modificando la velocidad Z de la entidad pelota"""
        #Modifica la velocidad directamente en los atributos de la pelota
        ball.vz -= (config.GRAVITY * dt)

    @staticmethod
    def _apply_friction(ball):
        """Aplica la fricción del aire en los ejes X e Y"""
        ball.vx *= config.FRICTION
        ball.vy *= config.FRICTION

    @staticmethod
    def _update_ball_position(ball, dt):
        """Actualiza la posición de la pelota basándose en su velocidad actual"""
        new_x = ball.x + (ball.vx * dt)
        new_y = ball.y + (ball.vy * dt)
        new_z = ball.z + (ball.vz * dt)
        ball.update_pos(new_x, new_y, new_z)

    @staticmethod
    def check_surface_collision(ball, limits):
        """
        Verifica colisión genérica con una superficie (como la mesa).
        Retorna un booleano (False si no hay, True si golpeó).
        """
        min_x, max_x, min_y, max_y, min_z, max_z = limits
        
        is_within_x = min_x <= ball.x <= max_x
        is_within_y = min_y <= ball.y <= max_y
        has_hit_surface = min_z <= ball.z <= max_z + ball.radius  # Consideramos el radio de la pelota para la colisión

        if is_within_x and is_within_y and has_hit_surface:
            #Rebotar la pelota e inyectar la nueva posición en el tope de la superficie
            ball.z = max_z + ball.radius
            ball.vz *= -ball.restitution
            return True 
        
        return False

    @staticmethod
    def check_floor_collision(ball):
        """
        Verifica la colisión con el piso.
        Retorna un booleano (False si no hay, True si golpeó).
        """
        if ball.z <= config.FLOOR_Z:
            ball.z = config.FLOOR_Z
            ball.vz *= -ball.restitution * 0.5  # Aplicamos un rebote más débil al piso
            return True
        return False

    @staticmethod
    def check_net_collision(ball, net_limits):
        """
        Verifica la colisión con la caja de la malla.
        Retorna un booleano (False si no hay, True si chocó).
        """
        min_x, max_x, min_y, max_y, min_z, max_z = net_limits
        
        if (min_x <= ball.x <= max_x and 
            min_y <= ball.y <= max_y and 
            min_z <= ball.z <= max_z):
            
            #Determinar dirección para posicionar la pelota fuera de la red
            if ball.vy > 0:
                ball.y = min_y
            else:
                ball.y = max_y
                
            ball.vy *= -config.NET_RESTITUTION
            ball.vz *= config.VERTICAL_BRAKING
            return True
        
        if (min_x <= ball.x <= max_x and 
            min_y <= ball.y <= max_y and 
            max_z <= ball.z <= max_z + ball.radius):
                
            ball.vz *= config.VERTICAL_BRAKING
            ball.vy *= config.VERTICAL_BRAKING
            ball.vx *= config.VERTICAL_BRAKING
            return True
            
        return False

    @staticmethod
    def check_paddle_collision(ball, paddle, dt):
        """Verifica la colisión tridimensional reactiva entre la pelota y cualquier raqueta"""
        cur_min_x, cur_max_x, cur_min_y, cur_max_y, cur_min_z, cur_max_z = paddle.get_limits()
        
        #Si la distancia real entre la pelota y la raqueta es muy grande, volvemos
        if math.dist((ball.x, ball.y, ball.z), (paddle.x, paddle.y, paddle.z)) > 25:
            return False
        

        #Donde estaba la raqueta en el frame anterior
        prev_min_x = cur_min_x - paddle.vx
        prev_max_x = cur_max_x - paddle.vx
        prev_min_y = cur_min_y - paddle.vy
        prev_max_y = cur_max_y - paddle.vy
        prev_min_z = cur_min_z - paddle.vz
        prev_max_z = cur_max_z - paddle.vz

        #Construimos el aabb barrido
        swept_min_x = min(prev_min_x, cur_min_x) - ball.radius
        swept_max_x = max(prev_max_x, cur_max_x) + ball.radius
        swept_min_y = min(prev_min_y, cur_min_y) - ball.radius
        swept_max_y = max(prev_max_y, cur_max_y) + ball.radius
        swept_min_z = min(prev_min_z, cur_min_z) - ball.radius
        swept_max_z = max(prev_max_z, cur_max_z) + ball.radius

        #Comprobacion AABB normal
        if (swept_min_x <= ball.x <= swept_max_x and
            swept_min_y <= ball.y <= swept_max_y and
            swept_min_z <= ball.z <= swept_max_z):
            

            current_restitution, other_restitution = paddle.get_restitution()
            z_factor = 0.2 #factor para que la velocidad de la raqueta al subir o bajar no rompa el juego
            speed_factor = 0.5

            if ball.y < paddle.y and paddle.vy < 0:
                ball.y = cur_min_y - ball.radius
                ball.vy = -abs(ball.vy)
                ball.vy += paddle.vy * other_restitution * speed_factor
                ball.vx += paddle.vx * other_restitution * speed_factor
                ball.vz += paddle.vz * other_restitution * z_factor
                            
            elif ball.y > paddle.y and paddle.vy > 0:
                ball.y = cur_max_y + ball.radius
                ball.vy = abs(ball.vy)
                ball.vy += paddle.vy * current_restitution * speed_factor
                ball.vx += paddle.vx * current_restitution * speed_factor
                ball.vz += paddle.vz * current_restitution * z_factor
            
            return True


        return False
    