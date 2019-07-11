/*----------------------------------------------------------
* COSC363  Ray Tracer
*
*  The cylinder class
*  This is a subclass of Object, and hence implements the
*  methods intersect() and normal().
-------------------------------------------------------------*/

#include "Cylinder.h"
#include <math.h>

/**
* Sphere's intersection method.  The input is a ray (pos, dir).
*/
float Cylinder::intersect(glm::vec3 posn, glm::vec3 dir)
{
    float a = pow(dir.x, 2) + pow(dir.z, 2);
    float b = 2 * (dir.x * (posn.x - center.x) + dir.z * (posn.z - center.z));
    float c = pow((posn.x - center.x), 2) + pow((posn.z - center.z), 2)- pow(radius, 2);

    //float k = 20.0
    //float a = pow(dir.x, 2) + pow(dir.z, 2);
    //float b = 2 * (dir.x * (posn.x - center.x) + dir.z * (posn.z - center.z));
    //float c = pow((posn.x - (center.x + k * posn.y)), 2) + pow((posn.z - center.z), 2)- pow(radius, 2);

    // quadratic equation
    float delta = b * b - 4 * (a * c);
    if(fabs(delta) < 0.001) return -1.0;
    if(delta < 0.0) return -1.0;

    float ts;
    float tb;
    float t1 = (-b - sqrt(delta)) / (2 * a);
    float t2 = (-b + sqrt(delta)) / (2 * a);

    if (t1 < 0.01) t1 = -1;
    if (t2 < 0.01) t2 = -1;

    if (t1 > t2) {
        ts = t2;
        tb = t1;
    }
    else {
        ts = t1;
        tb = t2;
    }

    float r = posn.y + ts * dir.y;

    if ((r >= center.y) and (r <= center.y + height)) return ts;
    else {
        float r = posn.y + dir.y * tb;
        if ((r >= center.y) && (r <= center.y + height)) return tb;
        else return -1.0;
    }
}

glm::vec3 Cylinder::normal(glm::vec3 p)
{
    //glm::vec3 n = glm::vec3 (((p.x - center.x) - k * p.y) ,0 ,(p.z - center.z));
    glm::vec3 n = glm::vec3 ((p.x - center.x) ,0 ,(p.z - center.z));
    n = glm::normalize(n);
    return n;
}
