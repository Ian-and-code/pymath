import types
import math
import sympy as sp

class Base:
    def __init__(self, base):
        self.digitos = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if base == 0 or base == 1:
            raise ValueError("Base inválida (no puede ser 0 ni 1)")
        if abs(base) > len(self.digitos):
            raise ValueError(f"Base demasiado grande (max {len(self.digitos)})")
        self.base = base

    # -------- Conversión a decimal ----------
    def to_10(self, num):
        if isinstance(num, (int, float)):
            return num
        num = str(num).upper()
        if "." in num:
            entero, frac = num.split(".")
            return self._to_10_entero(entero) + self._to_10_frac(frac)
        else:
            return self._to_10_entero(num)

    def _to_10_entero(self, s):
        raise NotImplementedError

    def _to_10_frac(self, frac):
        raise NotImplementedError

    # -------- Conversión desde decimal ----------
    def to_base(self, n, prec=10):
        raise NotImplementedError

    # -------- Operaciones ----------
    def plus(self, x, y):
        return self.to_base(self.to_10(x) + self.to_10(y))

    def minus(self, x, y):
        return self.to_base(self.to_10(x) - self.to_10(y))

    def times(self, x, y):
        return self.to_base(self.to_10(x) * self.to_10(y))

    def divide(self, x, y):
        return self.to_base(self.to_10(x) / self.to_10(y))

    def pow(self, x, y):
        return self.to_base(self.to_10(x) ** self.to_10(y))


# -----------------------------------
# Clase para bases positivas
class BaseP(Base):
    def _to_10_entero(self, s):
        return int(s, self.base) if s else 0

    def _to_10_frac(self, frac):
        val = 0
        for i, d in enumerate(frac):
            val += self.digitos.index(d) / (self.base ** (i+1))
        return val

    def to_base(self, n, prec=10):
        if n == 0:
            return "0"
        negativo = n < 0
        n = abs(n)
        entero = int(n)
        frac = n - entero

        # Parte entera
        res_ent = ""
        if entero == 0:
            res_ent = "0"
        else:
            while entero > 0:
                res_ent = self.digitos[entero % self.base] + res_ent
                entero //= self.base

        # Parte fraccionaria
        res_frac = ""
        if frac > 0:
            res_frac += "."
            for _ in range(prec):
                frac *= self.base
                dig = int(frac)
                res_frac += self.digitos[dig]
                frac -= dig
                if frac == 0:
                    break

        res = res_ent + res_frac
        if negativo:
            res = "-" + res
        return res


# -----------------------------------
# Clase para bases negativas
class BaseN(Base):
    def _to_10_entero(self, s):
        val = 0
        for i, d in enumerate(reversed(s)):
            val += self.digitos.index(d) * (self.base ** i)
        return val

    def _to_10_frac(self, frac):
        val = 0
        b = abs(self.base)
        for i, d in enumerate(frac):
            val += self.digitos.index(d) / (b ** (i+1))
        if len(frac) % 2 == 1:
            val = -val
        return val

    def to_base(self, n, prec=10):
        entero = int(n)
        frac = n - entero

        # Parte entera
        res_ent = ""
        if entero == 0:
            res_ent = "0"
        else:
            num = entero
            while num != 0:
                num, r = divmod(num, self.base)
                if r < 0:
                    num += 1
                    r -= self.base
                res_ent = self.digitos[r] + res_ent

        # Parte fraccionaria (aproximada)
        res_frac = ""
        if frac != 0:
            b = abs(self.base)
            res_frac += "."
            for _ in range(prec):
                frac *= b
                dig = int(frac)
                res_frac += self.digitos[dig]
                frac -= dig
                if frac == 0:
                    break

        return res_ent + res_frac
class cmpx:
    def __init__(self, r=0, m=0):
        self.r = r
        self.m = m
        self.value = r + m*1j  # para cálculos internos si hace falta

    # Representación bonita
    def __str__(self):
        if self.m == 0:
            return str(self.r)
        if self.r == 0:
            return f"{self.m}I"
        signo = '+' if self.m >= 0 else '-'
        return f"{self.r} {signo} {abs(self.m)}I"

    __repr__ = __str__

    # Helper para convertir otros tipos a cmpx
    @staticmethod
    def _to_cmpx(other):
        if isinstance(other, cmpx):
            return other
        elif isinstance(other, (int, float)):
            return cmpx(other, 0)
        elif isinstance(other, list) and len(other) == 2:
            return cmpx(other[0], other[1])
        elif isinstance(other, dict) and 'real' in other and 'imaginary' in other:
            return cmpx(other['real'], other['imaginary'])
        else:
            raise TypeError(f"No se puede convertir {other} a cmpx")

    # Operadores aritméticos
    def __add__(self, other):
        o = self._to_cmpx(other)
        return cmpx(self.r + o.r, self.m + o.m)

    def __sub__(self, other):
        o = self._to_cmpx(other)
        return cmpx(self.r - o.r, self.m - o.m)

    def __mul__(self, other):
        o = self._to_cmpx(other)
        r = self.r*o.r - self.m*o.m
        m = self.r*o.m + self.m*o.r
        return cmpx(r, m)

    def __truediv__(self, other):
        o = self._to_cmpx(other)
        denom = o.r**2 + o.m**2
        if denom == 0:
            raise ZeroDivisionError("División por cero")
        r = (self.r*o.r + self.m*o.m)/denom
        m = (self.m*o.r - self.r*o.m)/denom
        return cmpx(r, m)

    def __neg__(self):
        return cmpx(-self.r, -self.m)

    # Comparaciones (solo igualdad, para otras comparaciones habría que definir lógica)
    def __eq__(self, other):
        o = self._to_cmpx(other)
        return self.r == o.r and self.m == o.m

    # Opcional: soporte para +, -, *, / con lado derecho siendo otro tipo
    __radd__ = __add__
    __rsub__ = lambda self, other: cmpx._to_cmpx(other).__sub__(self)
    __rmul__ = __mul__
    __rtruediv__ = lambda self, other: cmpx._to_cmpx(other).__truediv__(self)

def integrate(f, v, i=None, s=None):
    if (i !=None and s != None) and (isinstance(i, int) and isinstance(s, int)):
        return sp.integrate(f, (v, i, s))
    else:
        return sp.integrate(f, v)

def derivate(f, v, o=1):
    return sp.derivate(f, v, o)

def delta(x):
    n = abs(int(x))
    delta_n = (n + ((n ** 2) + 4) ** 0.5)/2
    return delta_n

def nbonacci_phi(n, tol=1e-15, max_iter=1000):
    # Inicializamos cocientes aproximados
    ratio = 2.0
    prev = [1.0]*n
    for _ in range(max_iter):
        next_val = sum(prev)
        next_ratio = next_val / prev[-1]
        if abs(next_ratio - ratio) < tol:
            return next_ratio
        ratio = next_ratio
        prev = prev[1:] + [next_val]
    return ratio

def champernowne(base_class, base, terms=50, prec=200):
    b = base_class(base)
    s = ""
    for i in range(1, terms+1):
        s += b.to_base(i, 0)  # sin parte fraccionaria
    return "0." + s[:prec]

    ceinf = "".join(susce)
    c = 0 + (int(ceinf)/(base ** len(ceinf)))
    return c

def conv_angle(angle, actype, totype):
    return angle * (totype/actype)

def constshelp():
    consts = []
    for var, value in zip(globals().copy().keys(), globals().copy().values()):
        if isinstance(value, float):
            consts.append(var)
    return consts

def root(x, y=2):
    if x < 0:
        return cmpx(0, -x ** (1/y))
    return x ** (1/y)

def funcshelp():
    funcs = []
    for var, value in globals().copy().items():
        if isinstance(value, types.FunctionType):
            funcs.append(var)
    return funcs

def help():
    print(f"{funcshelp()} \n {constshelp()}")

sin = lambda x: math.sin(x)
cos = lambda x: math.cos(x)
tan = lambda x: math.tan(x)
cot = lambda x: 1 / math.tan(x)
sec = lambda x: 1 / math.cos(x)
csc = lambda x: 1 / math.sin(x)

Symbol = lambda s: sp.Symbol(s)
Symbols = lambda s: sp.symbols(s)
Expand = lambda e: sp.expand(e)

#hiperreales

inf = float('inf')
neginf = inf * -1
eps = 1e-20
negeps = eps * -1

# Constantes matemáticas
PI = 3.141592653589793
TAU = 2 * PI
EULER = 2.718281828459045


PHI = delta(1) # Número áureo
PHIcong = -(PHI-1)
delta2 = delta(2)
delta3 = delta(3)



CHAMPERNOWNE = champernowne(BaseP, 10, 102, 200)

CATALAN = 0.915965594177219  # Constante de Catalan
ZETA2 = 1.6449340668482264   # ζ(2) = π^2 / 6
ZETA4 = 1.082323233711138    # ζ(4) = π^4 / 90
GLAISHER = 1.2824271291006226  # Constante de Glaisher–Kinkelin
KAPREKAR = 6174              # Número de Kaprekar

# Constantes de teoría de números y análisis
EULER_MASCHERONI = 0.5772156649015329
SQRT_2 = 1.4142135623730951
SQRT_3 = 1.7320508075688772

# Constantes en grados y conversiones
RADIANS = TAU
DEGREES = 360
GRADIANS = 400



# Constantes que aparecen en la geometría
APERY_CONSTANT = 1.2020569031595942 # Suma de los recíprocos de los cubos de los números naturales

SQRT5 = 2.23606797749979      # Raíz cuadrada de 5
LEMNISCATE = 2.622057554292119 # Longitud de la lemniscata de Bernoulli
