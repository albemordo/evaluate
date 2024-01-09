provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "my_resgroup" {
  name     = "my_resgroup"
  location = "West Europe"
}

resource "azurerm_storage_account" "my_storage_account" {
  name                     = "my_storage_account"
  resource_group_name      = azurerm_resource_group.my_resgroup.name
  location                 = azurerm_resource_group.my_resgroup.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

}