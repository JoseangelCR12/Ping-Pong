import config
import math

class PhysicsEngine:
    
    @staticmethod
    def apply_gravity(ball, dt):
        """Aplica la gravedad modificando la velocidad Z de la entidad pelota"""
        #Modifica la velocidad directamente en los atributos de la pelota
        ball.vz -= (config.GRAVITY * dt)

    @staticmethod
    def apply_friction(ball):
        """Aplica la fricción del aire en los ejes X e Y"""
        ball.vx *= config.FRICTION
        ball.vy *= config.FRICTION

    @staticmethod
    def update_ball_position(ball, dt):
        """Actualiza la posición de la pelota basándose en su velocidad actual"""
        new_x = ball.x + (ball.vx * dt)
        new_y = ball.y + (ball.vy * dt)
        new_z = ball.z + (ball.vz * dt)
        ball.update_pos(new_x, new_y, new_z)

    @staticmethod
    def check_surface_collision(ball, limits):
        """
        Verifica colisión genérica con una superficie (como la mesa o el piso).
        Retorna un booleano (False si no hay, True si golpeó).
        """
        min_x, max_x, min_y, max_y, min_z, max_z = limits
        
        is_within_x = min_x <= ball.x <= max_x
        is_within_y = min_y <= ball.y <= max_y
        has_hit_surface = min_z <= ball.z <= max_z

        if is_within_x and is_within_y and has_hit_surface:
            #Rebotar la pelota e inyectar la nueva posición en el tope de la superficie
            ball.z = max_z
            ball.vz *= -ball.restitution
            return True #Contador de rebotes/colisiones para las gamerules
        
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
            
        return False

    @staticmethod
    def check_paddle_collision(ball, paddle, dt=1/60.0):
        """Verifica la colisión tridimensional reactiva entre la pelota y cualquier raqueta"""
        min_x, max_x, min_y, max_y, min_z, max_z, angle, twiddle = paddle.get_limits()

        # Comprobación de la caja de colisión (Hitbox) AABB en 3D
        if (min_x <= ball.x <= max_x and 
            min_y <= ball.y <= max_y and 
            min_z <= ball.z <= max_z):
            
            # Ajuste de posición para evitar que la pelota atraviese la raqueta en Y
            # Si el paddle es de la CPU (está en la mitad superior del mapa)
            if paddle.is_cpu:
                ball.y = min_y - 2  # Colocar la pelota justo en frente de la raqueta
                # Forzamos a que la pelota vaya hacia el jugador (-Y) combinando restituciones
                current_restitution = paddle.get_restitution()
                ball.vy = -abs(ball.vy) * current_restitution
            else:
                ball.y = max_y + 2  # Colocar la pelota en frente de la raqueta del jugador
                # Forzamos a que la pelota vaya hacia la CPU (+Y)
                current_restitution = paddle.get_restitution()
                ball.vy = abs(ball.vy) * current_restitution

            # Aplicamos la desviación trigonométrica reactiva por el ángulo físico
            angle_rad = math.radians(angle)
            base_impulse_y = paddle.vy * 1.0

            rotated_impulse_x = base_impulse_y * math.sin(angle_rad)
            rotated_impulse_y = base_impulse_y * math.cos(angle_rad)

            # Transferencia de velocidades reales acumuladas por el movimiento del paddle
            ball.vx += (paddle.vx * 0.5) + rotated_impulse_x
            ball.vy += rotated_impulse_y
            ball.vz += paddle.vz * 0.5
            
            return True
            
        return False