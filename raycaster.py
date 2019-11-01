import math
import pygame

def distances(objects, entity,screen,rad, display = True):


    #32 rays, 11.25 degrees between them
    s = [10000, 5.0273, 2.4142,
    1.4966, 1, 0.6682,
    0.4142, 0.1989, 0.000000001,
    -0.1989, -0.4142, -0.6682,
    -1, -1.4966, -2.4142,
    -5.0273, -10000, 5.0273,
    2.4142, 1.4966, 1,
    0.6682, 0.4142, 0.1989,
    -0.000000001, -0.1989, -0.4142,
    -0.6682, -1, -1.4966,
    -2.4142,-5.0273]

    touching = [rad] * 32

    for o in objects:
        for i in range (0,len(s)):

            visRadPoint = (math.cos(math.atan(s[i]))*entity.visRad+entity.x,math.sin(math.atan(s[i]))*entity.visRad+entity.y)

            #visradPoint is b, entity is a

            d = visRadPoint[1] - entity.y
            e = entity.x - visRadPoint[0]
            f = d*entity.x + e*entity.y

            #startpoint is C, endpoint is D
            a = o[1][1] - o[0][1]
            b = o[0][0] - o[1][0]
            c = a*o[0][0] + b*o[0][1]

            determinant = d*b - a*e

            if determinant == 0:
                continue

            x = (b*f - e*c)/determinant
            y = (d*c - a*f)/determinant
            intersect = (x,y)

            if o[0][0] < o[1][0]:
                if intersect[0] < o[0][0] or intersect[0] > o[1][0]:
                    continue

            elif o[0][0] > o[1][0]:
                if intersect[0] > o[0][0] or intersect[0] < o[1][0]:
                    continue
            if o[0][1] < o[1][1]:
                if intersect[1] < o[0][1] or intersect[1] > o[1][1]:
                    continue
            else:
                if intersect[1] > o[0][1] or intersect[1] < o[1][1]:
                    continue

            distance = math.sqrt((intersect[0]-entity.x)**2 + (intersect[1]-entity.y)**2)

            if distance <= entity.visRad and distance < touching[i]:
                if i <= 16 and intersect[0] - entity.x > 0:
                    touching[i] = distance
                elif i > 16 and intersect[0] - entity.x < 0:
                    touching[i] = distance








    if display:
        for i in range(len(touching)):

            m = 1

            if i > 16:
                m = -1

            a = math.atan(s[i])

            pygame.draw.line(screen, (237, 122, 255), (entity.x, entity.y),(entity.x+m*int(math.cos(a)*entity.visRad),entity.y+m*int(math.sin(a)*entity.visRad)),1)

            if touching[i] != rad:
                pygame.draw.circle(screen,(252, 186, 3),(int(m*math.cos(a)*touching[i]+entity.x), int(m*math.sin(a)*touching[i]+entity.y)),4)


    return touching
