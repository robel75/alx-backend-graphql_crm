import graphene
from crm.models import Product

class ProductType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    stock = graphene.Int()

class UpdateLowStockProducts(graphene.Mutation):
    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        updated = []
        low_stock_products = Product.objects.filter(stock__lt=10)
        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated.append(product)
        return UpdateLowStockProducts(updated_products=updated, message="Low stock products updated")
