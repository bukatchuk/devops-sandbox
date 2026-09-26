variable "name_prefix" {
  description = "Префикс имён ресурсов"
  type        = string
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{1,20}$", var.name_prefix))
    error_message = "Только строчные буквы, цифры и дефис, 2–21 символ."
  }
}

variable "image" {
  description = "Образ контейнера с явным тегом (не latest)"
  type        = string
  default     = "nginx:1.29-alpine"
}

variable "replicas" {
  description = "Число контейнеров"
  type        = number
  default     = 1
  validation {
    condition     = var.replicas >= 1 && var.replicas <= 5
    error_message = "Допустимо от 1 до 5 реплик."
  }
}
