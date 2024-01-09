provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "my_resgroup" {
  name     = "my_resgroup"
  location = "West Europe"
}

resource "azurerm_network_security_group" "my_secgroup" {
  name                = "my_secgroup"
  location            = azurerm_resource_group.my_resgroup.location
  resource_group_name = azurerm_resource_group.my_resgroup.name
}