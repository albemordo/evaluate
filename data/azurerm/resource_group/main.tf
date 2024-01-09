provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "my_resgroup" {
  name     = "my_resgroup"
  location = "West Europe"
}