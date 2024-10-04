import scrapy


class RunningShoesSpider(scrapy.Spider):
    name = "running_shoes"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_pages = 10

    def parse(self, response):
        products = response.css("div.poly-card__content")

        for product in products:
            prices = product.css("span.andes-money-amount__fraction::text").getall()
            cents = product.css(
                "span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text"
            ).getall()

            data = {
                "brand": product.css("span.poly-component__brand::text").get(),
                "name": product.css("h2.poly-box.poly-component__title a::text").get(),
                "new_price_reais": prices[1] if len(prices) > 1 else None,
                "new_price_centavos": cents[1] if len(cents) > 1 else None,
                "old_price_reais": prices[0] if len(prices) > 0 else None,
                "old_price_centavos": cents[0] if len(cents) > 0 else None,
                "reviews_rating_number": product.css(
                    "span.poly-reviews__rating::text"
                ).get(),
                "reviews_amount": product.css("span.poly-reviews__total::text").get(),
            }

            if not product.css(
                "s.andes-money-amount.andes-money-amount--previous.andes-money-amount--cents-comma"
            ):
                data["new_price_reais"] = prices[0] if len(prices) > 0 else None
                data["new_price_centavos"] = cents[0] if len(cents) > 0 else None
                data["old_price_reais"] = None
                data["old_price_centavos"] = None

            yield data

        if self.page_count < self.max_pages:
            next_page = response.css(
                "li.andes-pagination__button.andes-pagination__button--next a::attr(href)"
            ).get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
