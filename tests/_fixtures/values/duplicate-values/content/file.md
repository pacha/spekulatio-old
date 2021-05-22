---

# duplicate value at same scope
foo: 1
foo: 2
foo: 3

# duplicate value at different scopes
__bar:
  scope: branch
  value: 1

__bar:
  scope: local
  value: 2

__baz:
  scope: local
  value: 1

__baz:
  scope: branch
  value: 2

---

