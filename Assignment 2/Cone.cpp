/*----------------------------------------------------------
* COSC363  Ray Tracer
*
* The cone class
* This is a subclass of Object, and hence implements the
* methods intersect() and normal().
-------------------------------------------------------------*/

#include "Cone.h"
#include <math.h>

/**
* Cone's intersection method.  The input is a ray (pos, dir).
*/
float Cone::intersect(glm::vec3 pos, glm::vec3 dir)
{
    glm::vec3 d = pos - center;
    float yd = height - pos.y + center.y;
    float stan = pow((radius / height), 2);
    float a = (dir.x * dir.x) + (dir.z * dir.z) - (stan*(dir.y * dir.y));
    float b = 2 * (d.x * dir.x + d.z * dir.z + stan*yd*dir.y);
    float c = pow(d.x, 2) + pow(d.z, 2) - (stan * pow(yd, 2));
    float delta = b * b-4*(a*c);

    if(fabs(delta) < 0.001) return -1.0;
    if(delta < 0.0) return -1.0;

    float ts;
    float tb;
    float t1 = (-b - sqrt(delta))/(2*a);
    float t2 = (-b + sqrt(delta))/(2*a);

    if(t1 < 0.01) t1=-1;
    if(t2<0.01) t2=-1;

    if (t1 > t2){
        ts = t2;
        tb = t1;
    } else {
        ts = t1;
        tb = t2;
    }

    float ypos = pos.y + dir.y * ts;
    if((ypos >= center.y) && (ypos <= center.y + height)){
        return ts;
    }
    else{
        float ypos = pos.y + dir.y * tb;
        if((ypos >= center.y) && (ypos <= center.y + height)){
            return tb;
        }else{
            return -1.0;
    }
}
}
/**
* Returns the unit normal vector at a given point.
*/
glm::vec3 Cone::normal(glm::vec3 p)
{
    float r = sqrt(pow(p.x - center.x, 2) + pow((p.z - center.z), 2));
    glm::vec3 n= glm::vec3 (p.x - center.x, r * (radius/height), p.z - center.z);
    n=glm::normalize(n);
    return n;
}
