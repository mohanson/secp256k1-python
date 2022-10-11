import secp256k1

# Sony uses a private key, typically stored (in an HSM?) at the company's HQ, to mark their Playstation firmwares as
# valid and unmodified. The PS3 only needs a public key to verify that the signature came from Sony. Normally, this is
# considered safe; but Sony did a rookie mistake in the implementation of their signing algorithm - they used the same
# random number to sign everything.
#
# Recall how the (public parameter) r in the signature is generated from a (secret) random number k, using the formula
# kG = R, r being the x-coordinate of the point R. Given two signatures that use the same k,  prove how you can extract
# the private key used for signing. Use the signature formula in the ECDSA section. You'll need pen and paper for this.

m1 = 0x72a963cdfb01bc37cd283106875ff1f07f02bc9ad6121b75c3d17629df128d4e
r1 = 0x741a1cc1db8aa02cff2e695905ed866e4e1f1e19b10e2b448bf01d4ef3cbd8ed
s1 = 0x2222017d7d4b9886a19fe8da9234032e5e8dc5b5b1f27517b03ac8e1dd573c78

m2 = 0x059aa1e67abe518ea1e09587f828264119e3cdae0b8fcaedb542d8c287c3d420
r2 = 0x741a1cc1db8aa02cff2e695905ed866e4e1f1e19b10e2b448bf01d4ef3cbd8ed
s2 = 0x5c907cdd9ac36fdaf4af60e2ccfb1469c7281c30eb219eca3eddf1f0ad804655


class Fr:
    def __init__(self, x):
        assert(0 <= x < secp256k1.N)
        self.x = x

    def __repr__(self):
        return f'Fr(0x{self.x:064x})'

    def __eq__(self, other):
        return self.x == other.x

    def __add__(self, other):
        return Fr((self.x + other.x) % secp256k1.N)

    def __sub__(self, other):
        return Fr((self.x - other.x) % secp256k1.N)

    def __mul__(self, other):
        return Fr((self.x * other.x) % secp256k1.N)

    def __div__(self, other):
        return self * other ** -1

    def __pow__(self, other):
        return Fr(pow(self.x, other, secp256k1.N))

    def __neg__(self):
        return Fr(secp256k1.N - self.x)


Fr.__truediv__ = Fr.__div__

# Formula:
# s1 = (m1 + prikey * r1) / k
# s2 = (m2 + prikey * r2) / k = (m2 + prikey * r1) / k
# s1 / s2 = (m1 + prikey * r1) / (m2 + prikey * r1)
# prikey = (s1 * m2 - s2 * m1) / (s2 - s1) / r1

prikey = (Fr(s1) * Fr(m2) - Fr(s2) * Fr(m1)) / (Fr(s2) - Fr(s1)) / Fr(r1)
assert prikey.x == 0x5f6717883bef25f45a129c11fcac1567d74bda5a9ad4cbffc8203c0da2a1473c
