line = readline()
n = 14
for (i, c) in enumerate(line)
  chunk = Set(line[i:i+n-1])
  if length(chunk) == n
    println(i + n - 1)
    break
  end
end
