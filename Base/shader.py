import numpy as np

import argparse
import subprocess
import os
import random

class Material():
    def __init__(self):
        pass

    def f(self, wi, wo, n):
        pass

    def __add__(self, other):
        result = Material()
        def f(wi, wo, n):
            return self.f(wi,wo,n) + other.f(wi,wo,n)
        result.f = f
        return result

class Lambert(Material):
    def __init__(self, albedo, diffuse):
        super().__init__()
        self.albedo = np.array(albedo)
        self.diffuse = diffuse
    
    def f(self, wo, wi, n):
        return self.albedo * self.diffuse / np.pi
    


class BlinnPhong(Material):
    def __init__(self,diffuse,shine):
        super().__init__()
        self.diffuse = np.array(diffuse)
        self.shine = shine

    def f(self, wo, wi, n):
        mid = wo + wi
        wh = mid / np.linalg.norm(mid, axis=-1, keepdims=True)
        nwh = np.sum(n*wh, axis=-1, keepdims=True)
        return self.diffuse * nwh**self.shine

class Cook(Material):
    def __init__(self, alpha, specular, metal):
        self.alpha = alpha
        self.roughness = np.sqrt(self.alpha)
        self.k = (self.roughness + 1)**2/8
        self.F0 = metal
        self.spec = np.array(specular)
    

    def f(self, wo, wi, n):
        mid = wo + wi
        wh = mid / np.linalg.norm(mid)

        nwh = np.sum(n*wh, axis=-1, keepdims=True)
        nwi = np.sum(n*wi, axis=-1, keepdims=True)
        nwo = np.sum(n*wo, axis=-1, keepdims=True)

        D = self.alpha**2 / (np.pi *(nwh**2*(self.alpha**2-1)+1)**2)

        k = (self.roughness + 1)**2 / 8
        
        Gi = nwi/(nwi*(1-k)+k)
        Go = nwo/(nwo*(1-k)+k)

        G = Gi * Go

        c1 = -5.55473
        c2 = -6.98316
        oh = np.sum(wh * wo, axis=-1, keepdims=True)
        F = self.spec * (self.F0 + (1 - self.F0)*2**((c1*oh + c2)*oh))

        F[(nwi <= 0).squeeze()] = 0

        return D*F*G/(4 * nwi * nwo + 1e-10)
        

    
class LightSource():
    def __init__(self, position, color, intensity):
        self.position = np.array(position)
        self.color = np.array(color)
        self.intensity = intensity
    
    def set_position(self, position):
        self.position = np.array(position)


def shade(normal, xyz, cam, material, lights):
    nlig, ncol, _ = normal.shape
    render = np.zeros((nlig, ncol, 3))

    i,j = np.meshgrid(range(nlig), range(ncol),indexing='ij')
    i = -(2*i - nlig)/nlig
    j = (2*j - ncol)/nlig

    wo = cam.reshape(1,1,3) - xyz
    wo = wo / np.linalg.norm(wo, axis=-1, keepdims=True)

    for light in lights:
        wi = light.position - xyz
        wi = wi / np.linalg.norm(wi, axis=-1, keepdims=True)

        f = material.f(wo, wi, normal)

        Li = light.intensity * light.color
        nwi = np.sum(normal*wi,axis=-1,keepdims=True)
        res = f * Li * nwi
        render += np.clip(f*Li*nwi, 0, None)
    return render

def clip_render(render, perc=5):
    low = np.percentile(render, perc)
    high = np.percentile(render, 100-perc)

    render = np.clip(render, low, high)
    render -= low
    render /= (high - low)
    return 255 * render

if __name__ == "__main__":
    
    
    # Define materials
    if args.cook:
        LMin,  LMax = 45, 55
        material = Cook(5, [0.8,0.42,0.42], 0.02)
    elif args.blinn:
        LMin,  LMax = 0.5, 0.75
        material = BlinnPhong([0.80,0.42,0.42],5) + Lambert([0.42,0.42,0.42],2)
    elif args.lambert:
        LMin,  LMax = 0.5, 0.75
        material = Lambert([0.42,0.42,0.42],2)
    else:
        print("No material selected")
    
    
    light_intensity = lambda : LMin + (LMax - LMin) * np.random.random(1)
    light_color = lambda : 0.5 + 0.5 *np.random.random(3)
    light_pos = lambda : [-1 + 2* random.random(),-1 + 2* random.random(),0.5]
