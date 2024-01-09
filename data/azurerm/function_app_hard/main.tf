provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "my_resgroup" {
  name     = "my_resgroup"
  location = "West Europe"
}

resource "azurerm_service_plan" "my_service_plan" {
  name                = "my_service_plan"
  resource_group_name = azurerm_resource_group.my_resgroup.name
  location            = azurerm_resource_group.my_resgroup.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "my_function_app" {
  name                = "my_function_app"
  resource_group_name = azurerm_resource_group.my_resgroup.name
  location            = azurerm_resource_group.my_resgroup.location

  service_plan_id            = azurerm_service_plan.my_service_plan.id

  site_config {}
}