Some C++ code for you

``` c++ title="hi" hl_lines="2 3"
 
auto ExtractRef(auto&& Val)
{
    auto* Address = &Val;
    Address->XPos = 40.0;
    return std::decay_t<decltype(Val)>();
}
```

``` py
def val() -> int
    return 5
```