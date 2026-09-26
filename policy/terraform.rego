# Политика для плана Terraform (terraform show -json).
# Проверяется conftest/OPA: провайдеро-независимый шлюз качества.
package main

import rego.v1

# Собираем создаваемые/меняемые ресурсы из плана.
resources contains rc if {
	some rc in input.resource_changes
	rc.change.actions[_] != "delete"
}

# 1. Образ не должен использовать тег :latest или быть без тега.
deny contains msg if {
	some rc in resources
	rc.type == "docker_image"
	name := rc.change.after.name
	endswith(name, ":latest")
	msg := sprintf("образ %q использует тег latest — закрепите версию", [name])
}

deny contains msg if {
	some rc in resources
	rc.type == "docker_image"
	name := rc.change.after.name
	not contains(name, ":")
	msg := sprintf("образ %q без тега — закрепите версию", [name])
}

# 2. Контейнер должен иметь политику перезапуска (не "no").
deny contains msg if {
	some rc in resources
	rc.type == "docker_container"
	policy := object.get(rc.change.after, "restart", "no")
	policy == "no"
	msg := sprintf("контейнер %q без политики перезапуска", [rc.change.after.name])
}
