output "container_names" {
  description = "Имена созданных контейнеров"
  value       = docker_container.web[*].name
}

output "count" {
  description = "Число контейнеров"
  value       = length(docker_container.web)
}
