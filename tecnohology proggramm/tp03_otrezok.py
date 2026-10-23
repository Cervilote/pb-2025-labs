
import math

EPS = 1e-9

class Point:

    __slots__ = ("_x", "_y")

    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def shifted(self, v):
        return Point(self._x + v.x, self._y + v.y)

    def distance_to(self, other):
        return math.hypot(self._x - other.x, self._y - other.y)

    def __eq__(self, other):
        return (isinstance(other, Point)
                and self._x == other._x and self._y == other._y)

    def __hash__(self):
        return hash(("Point", self._x, self._y))

    def __repr__(self):
        return f"Point({self._x:g}, {self._y:g})"

class Vector:

    __slots__ = ("_x", "_y")

    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def plus(self, other):
        return Vector(self._x + other.x, self._y + other.y)

    def __eq__(self, other):
        return (isinstance(other, Vector)
                and self._x == other._x and self._y == other._y)

    def __hash__(self):
        return hash(("Vector", self._x, self._y))

    def __repr__(self):
        return f"Vector({self._x:g}, {self._y:g})"

class Segment:

    __slots__ = ("_a", "_b")

    def __init__(self, p, q):
        if p == q:
            raise ValueError("вырожденный отрезок: концы должны различаться")
        self._a = p
        self._b = q

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    def length(self):
        return self._a.distance_to(self._b)

    def midpoint(self):
        return Point((self._a.x + self._b.x) / 2.0,
                     (self._a.y + self._b.y) / 2.0)

    def direction(self):
        return Vector(self._b.x - self._a.x, self._b.y - self._a.y)

    def shifted(self, v):
        return Segment(self._a.shifted(v), self._b.shifted(v))

    def contains(self, r):
        ab = self.direction()
        ar = Vector(r.x - self._a.x, r.y - self._a.y)
        len_sq = self.length() ** 2
        tol = EPS * max(1.0, len_sq)
        cross = ab.x * ar.y - ab.y * ar.x
        if abs(cross) > tol:
            return False
        dot = ar.x * ab.x + ar.y * ab.y
        return -tol <= dot <= len_sq + tol

    def __eq__(self, other):
        if not isinstance(other, Segment):
            return False
        return ((self._a == other._a and self._b == other._b)
                or (self._a == other._b and self._b == other._a))

    def __hash__(self):
        ends = sorted([(self._a.x, self._a.y), (self._b.x, self._b.y)])
        return hash(("Segment", ends[0], ends[1]))

    def __repr__(self):
        return f"Segment({self._a!r}, {self._b!r})"


def test_pred_uslovie_sozdat_ravnye_koncy_otkaz():
    p = Point(1.0, 2.0)
    try:
        Segment(p, Point(1.0, 2.0))
    except ValueError:
        pass
    else:
        raise AssertionError("создать(p, p) должен отклоняться ValueError")


def test_invariant_koncy_razlichny_posle_sdviga():
    s = Segment(Point(0, 0), Point(4, 0)).shifted(Vector(7, -3))
    assert s.a != s.b


def test_invariant_dlina_neotricatelna():
    s = Segment(Point(-5, -2), Point(9, 7))
    assert s.length() >= 0


def test_invariant_neizmenyaemost_sdvig_ne_menyaet_ishodny():
    s = Segment(Point(1, 1), Point(3, 1))
    s.shifted(Vector(2, -1))
    assert s.a == Point(1, 1) and s.b == Point(3, 1)


def test_post_uslovie_dliny_teorema_pifagora():
    s = Segment(Point(0, 0), Point(3, 4))
    assert math.isclose(s.length(), 5.0)


def test_post_uslovie_seredina_tochno():
    s = Segment(Point(-2, 1), Point(6, 5))
    assert s.midpoint() == Point(2.0, 3.0)


def test_post_uslovie_napravlyayushiy_raven_raznosti():
    s = Segment(Point(1, 2), Point(4, 6))
    assert s.direction() == Vector(3.0, 4.0)


def test_post_uslovie_sdvig_rovno_na_v():
    s = Segment(Point(1, 1), Point(3, 1))
    t = s.shifted(Vector(2, -1))
    assert t.a == Point(3, 0) and t.b == Point(5, 0)


def test_post_uslovie_soderzhit_koncy_i_seredinu():
    s = Segment(Point(0, 0), Point(4, 2))
    assert s.contains(s.a) and s.contains(s.b)
    assert s.contains(s.midpoint())


def test_post_uslovie_ne_soderzhit_vne_otrezka():
    s = Segment(Point(0, 0), Point(4, 2))
    assert not s.contains(Point(10, 5))
    assert not s.contains(Point(1, 3))


def test_post_uslovie_ravenstvo_bez_poryadka_koncov():
    s = Segment(Point(0, 0), Point(4, 2))
    t = Segment(Point(4, 2), Point(0, 0))
    assert s == t
    assert s != Segment(Point(0, 0), Point(4, 3))


def test_tochka_rasstoyanie_do_sebya_nol():
    p = Point(3, 4)
    assert p.distance_to(p) == 0


def test_tochka_rasstoyanie_simmetrichno():
    p, q = Point(1, 2), Point(4, 6)
    assert p.distance_to(q) == q.distance_to(p)


def test_tochka_sdvig_ne_menyaet_ishodnuyu():
    p = Point(1, 1)
    q = p.shifted(Vector(2, -1))
    assert q == Point(3, 0)
    assert p == Point(1, 1)


def test_vektor_summa_pokomponentno():
    assert Vector(1, 2).plus(Vector(3, 4)) == Vector(4, 6)


def _run_all_tests():
    tests = sorted(
        (name, fn) for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    )
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"OK    {name}")
        except AssertionError as err:
            failed += 1
            print(f"FAIL  {name}: {err}")
        except Exception as err:
            failed += 1
            print(f"ERROR {name}: {type(err).__name__}: {err}")
    print(f"\nИтог: прошли {len(tests) - failed} из {len(tests)} тестов")
    return failed == 0


def _demo():
    s = Segment(Point(0, 0), Point(3, 4))
    print("Отрезок:", s)
    print("Длина:", s.length())
    print("Середина:", s.midpoint())
    print("Направляющий вектор:", s.direction())
    print("Содержит (1.5, 2)?", s.contains(Point(1.5, 2)))
    print("Содержит (10, 5)?", s.contains(Point(10, 5)))
    print("Сдвиг на (1, 1):", s.shifted(Vector(1, 1)))
    print("Исходный не изменился:", s)


if __name__ == "__main__":
    print("Запуск тестов (написаны по спецификации, до реализации)...\n")
    ok = _run_all_tests()
    print("\nДемонстрация операций:")
    _demo()
    raise SystemExit(0 if ok else 1)
