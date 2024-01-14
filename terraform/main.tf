variable "variable_1" {
  default = "Hello World!"
}

output "output_1" {
  value = variable.variable_1
}