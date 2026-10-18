from sympy import isprime, gcd

#ezt mind egy sorban igen XD

def are_valid_rsa_parameters(p:int , q:int, d:int, e:int):
    if isprime(p) and isprime(q) and p!=q and e > 2 and e < (p-1)*(q-1) and gcd(e, (p-1)*(q-1)) == 1 and (e*d) % ((p-1)*(q-1)) == 1:
        return True
    return False

if __name__ == "__main__":

  tests = [
      (True, (854383, 911683, 559913054987, 519917050283)),
      (False, (853342, 11981, 3558587207, 3377232503)),
      (False, (291491, 717009, 16867459923, 11513965147)),
      (False, (955793, 955793, 727168494075, 193855182131)),
      (False, (898133, 222043, 1, 16153265069065)),
      (False, (758491, 882913, 553159763449, 130177488607))
  ]

  for test in tests:
    try:
      assert test[0] == are_valid_rsa_parameters(*test[1])
    except NotImplementedError:
      print(f"are_valid_rsa_parameters: not implemented")
      exit(1)
    except AssertionError as message:
      print(f"are_valid_rsa_parameters: FAILED ({message})")
      exit(1)
  print(f"are_valid_rsa_parameters: OK")