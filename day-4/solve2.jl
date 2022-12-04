lines = eachline()

total = 0
for line in lines
  r1, r2 = split(line, ',')
  a, b = split(r1, '-') |> x -> parse.(Int, x)
  c, d = split(r2, '-') |> x -> parse.(Int, x)
  if (a >= c && a <= d) || (b >= c && b <= d) || (c >= a && c <= b) || (d >= a && d <= b)
    global total += 1
  end
end

total |> println
