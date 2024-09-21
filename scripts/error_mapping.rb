class FuncDescriptor
  attr_accessor :owning_type, :policy_map, :error_code_map
end
name = "OK"

puts %{Some #{name} was here.}
#5.times { |i| puts "Eating #{i+1}." }