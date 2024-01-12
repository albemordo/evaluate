provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "my_resgroup" {
  name     = "example-resources"
  location = "West Europe"
}

resource "azurerm_virtual_network" "my_vpc" {
  name                = "my_vpc"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.my_resgroup.location
  resource_group_name = azurerm_resource_group.my_resgroup.name
}

resource "azurerm_subnet" "my_subnet" {
  name                 = "my_subnet"
  resource_group_name  = azurerm_resource_group.my_resgroup.name
  virtual_network_name = azurerm_virtual_network.my_vpc.name
  address_prefixes     = ["10.0.1.0/24"]
}