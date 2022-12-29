using Printf # @printf c-style

function main()
  inp = readline()
  santa = (0, 0)
  robot = (0, 0)
  dirs = Dict{Char,Tuple{Int,Int}}(
    '^' => (-1, 0),
    '>' => (0, 1),
    'v' => (1, 0),
    '<' => (0, -1)
  )

  seen = Set{Tuple{Int,Int}}([santa, robot])

  for idx in 1:2:length(inp)-1 # start:step:end
    Δsanta = dirs[inp[idx]] # \Delta
    Δrobot = dirs[inp[idx+1]]
    santa = santa .+ Δsanta # element-wise addition
    robot = robot .+ Δrobot
    union!(seen, [santa, robot]) # preferable to two push!'s
  end

  @printf "Length of set is %d\n" length(seen)

end

main()
