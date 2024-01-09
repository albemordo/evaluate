provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "my_resgroup" {
  name     = "my_resgroup"
  location = "West Europe"
}

resource "azurerm_virtual_network" "my_vpc" {
  name                = "my_vpc"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.my_resgroup.location
  resource_group_name = azurerm_resource_group.my_resgroup.name
}