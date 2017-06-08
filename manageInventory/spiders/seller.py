    # -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request
import re


class ManageInventorySpider(scrapy.Spider):
    name = "seller"
    allowed_domains = ["sellercentral.amazon.com", "catalog.amazon.com"]
    start_urls = ['https://sellercentral.amazon.com/']

    def __init__(self, *args, **kwargs):
        super(ManageInventorySpider, self).__init__(*args, **kwargs)
        self.pid = kwargs.get('asin').split(',')

    def parse(self, response):

        signin_form = response.xpath('//form[@name="signIn"]')
        hidden_field_names = signin_form.xpath('.//*[@type="hidden"]/@name').extract()
        hidden_field_values = signin_form.xpath('.//*[@type="hidden"]/@value').extract()
        hidden_agg = dict(zip(hidden_field_names, hidden_field_values))
        hidden_agg['email'] = 'chintom'
        hidden_agg['password'] = '20fg09'
        return FormRequest.from_response(response,
                                         formdata=hidden_agg,
                                         callback=self.parse_selection)

    def parse_selection(self, response):
        print("############################")
        #                       HomePAge: Amazon Selling Coach
        home_text=response.xpath('//*[@id="widget-fuJi9w"]/div/div[1]/h2/text()').extract_first()
        print(home_text)
        #                       Captcha Page:
        captchapage_text=response.xpath('//*[@id="ap_captcha_title"]/h2/text()').extract_first()  # Type charectors you....
        captcha_src=response.xpath('//*[@id="ap_captcha_img"]/img/@src').extract_first()          # CaptchaImage xpath
        print(captcha_src)
        print(captchapage_text)
        print("********#############********")
        #                       Incorrect Password:
        incorect_text=response.xpath('//*[@id="message_error"]/p/text()').extract_first()  # Your Password is Incorrect
        print(incorect_text)
        print("******************************")


        if captchapage_text is not None:
            print("Captcha Page")
            print(captchapage_text)
            print(captcha_src)

        if incorect_text is not None:
            print(incorect_text)



        if home_text is not None:
            print(home_text)
            asin_id = self.pid[0]
            search_url = 'https://sellercentral.amazon.com/inventory/ref=ag_invmgr_dnav_xx_?tbla_myitable=sort:%7B%22sortOrder%22%3A%22DESCENDING%22%2C%22sortedColumnId%22%3A%22date%22%7D;search:BBBBBBBBBB;pagination:1;'
            next_page_url = re.sub('BBBBBBBBBB', asin_id, search_url)
            yield Request(url=next_page_url,
                          callback=self.parse_manage_inventory)









    """

    def scrape_home(self, response):
        
        
        asin_id=self.pid[0]
        search_url = 'https://sellercentral.amazon.com/inventory/ref=ag_invmgr_dnav_xx_?tbla_myitable=sort:%7B%22sortOrder%22%3A%22DESCENDING%22%2C%22sortedColumnId%22%3A%22date%22%7D;search:BBBBBBBBBB;pagination:1;'
        next_page_url=re.sub('BBBBBBBBBB', asin_id, search_url)
        yield Request(url=next_page_url,
                      callback=self.parse_manage_inventory)


    """
    
    
    
    
    def parse_manage_inventory(self, response):

        option_tag = response.xpath('//div[@class="mt-save-button-dropdown-normal"]/span/select/option[1]').extract_first()
        url_list = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                              option_tag)
        url_to_edit_info = url_list[0].replace("amp;", "")
        yield Request(url=url_to_edit_info,
                      callback=self.parse_edit_info)

    def parse_edit_info(self, response):
        #print("-------Edit Product Info Page----url")
                            # Text Label Names From Inspected Code
        js_t_label=['item_name', 'manufacturer', 'model', 'part_number', 'color_name', 'color_map', 'size_name', 'size_map',
         'brand_name', 'related_product_id', 'external_product_id', 'legal_compliance_certification_metadata',
         'legal_compliance_certification_expiration_date', 'item_sku', 'merchant_release_date', 'import_designation',
         'product_tax_code', 'standard_price', 'sale_price', 'sale_from_date', 'sale_end_date', 'offering_start_date',
         'bullet_point1', 'bullet_point2', 'bullet_point3', 'bullet_point4', 'bullet_point5', 'platinum_keywords1',
         'platinum_keywords2', 'platinum_keywords3', 'platinum_keywords4', 'platinum_keywords5', 'generic_keywords1',
         'generic_keywords2', 'generic_keywords3', 'generic_keywords4', 'generic_keywords5',
         'target_audience_keywords1', 'target_audience_keywords2', 'target_audience_keywords3',
         'target_audience_keywords4', 'target_audience_keywords5', 'thesaurus_subject_keywords1',
         'thesaurus_subject_keywords2', 'thesaurus_subject_keywords3', 'thesaurus_subject_keywords4',
         'thesaurus_subject_keywords5', 'thesaurus_attribute_keywords1', 'thesaurus_attribute_keywords2',
         'thesaurus_attribute_keywords3', 'thesaurus_attribute_keywords4', 'thesaurus_attribute_keywords5',
         'specific_uses_keywords1', 'specific_uses_keywords2', 'specific_uses_keywords3', 'specific_uses_keywords4',
         'specific_uses_keywords5', 'item_display_width', 'item_display_depth', 'item_display_diameter',
         'item_display_height', 'item_display_length', 'item_display_weight', 'seat_height', 'list_price',
         'item_length', 'item_height', 'item_width', 'item_weight', 'website_shipping_weight', 'itemTypeDisplay',
         'pattern_name', 'style_name', 'material_type', 'wattage', 'country_string', 'warranty_description',
         'volume_capacity_name', 'blade_material_type', 'blade_edge_type', 'blade_length', 'product_site_launch_date',
         'package_length', 'package_height', 'package_width', 'package_weight', 'included_components1',
         'included_components2', 'included_components3', 'included_components4', 'included_components5',
         'lithium_battery_energy_content', 'special_features1', 'special_features2', 'special_features3',
         'special_features4', 'special_features5', 'lithium_battery_voltage', 'lithium_battery_weight', 'occasion_type',
         'item_shape', 'catalog_number', 'finish_type', 'specification_met', 'external_testing_certification',
         'matte_style', 'fur_description', 'fabric_type1', 'fabric_type2', 'fabric_type3',
         'cpsia_cautionary_description']
                             # Text Label Names from UI
        ui_text_label=[' Product Name', ' Manufacturer', ' Model Number', ' Manufacturer Part Number', ' Color',
         ' Color Map',' Size', ' Size Map', ' Brand Name', ' Related Product ID', ' Product ID',
         ' Please provide the Executive Number (EO) required for sale into California.',
         ' Please provide the expiration date of the EO Number.', ' Seller SKU', ' Release Date', ' Import Designation',
         ' Product Tax Code', ' Your price', ' Sale Price', ' Sale Start Date', ' Sale End Date',
         ' Offering Release Date', ' Key Product Features1', ' Key Product Features2', ' Key Product Features3',
         ' Key Product Features4', ' Key Product Features5', ' Platinum Keywords1', ' Platinum Keywords2',
         ' Platinum Keywords3', ' Platinum Keywords4', ' Platinum Keywords5', ' Search Terms1', ' Search Terms2',
         ' Search Terms3', ' Search Terms4', ' Search Terms5', ' Target Audience1', ' Target Audience2',
         ' Target Audience3', ' Target Audience4', ' Target Audience5', ' Subject Matter1', ' Subject Matter2',
         ' Subject Matter3', ' Subject Matter4', ' Subject Matter5', ' Other Attributes1', ' Other Attributes2',
         ' Other Attributes3', ' Other Attributes4', ' Other Attributes5', ' Intended Use1', ' Intended Use2',
         ' Intended Use3', ' Intended Use4', ' Intended Use5', ' Item Display Width', ' Item Display Depth',
         ' Item Display Diameter', ' Item Display Height', ' Item Display Length', ' Item Display Weight',
         ' Seat Height', " Manufacturer's Suggested Retail Price", ' Item Length', ' Item Height', ' Item Width',
         ' Weight', ' Shipping Weight', ' Category (item-type)', ' Design', ' Style Name', ' Material Type', ' Wattage',
         ' Country of Origin', ' Manufacturer Warranty Description', ' Volume', ' Blade Material Type', ' BladeType',
         ' BladeLength', ' Launch Date', ' Package Length', 'Package Height', 'Package Width', 'Package Weight',
         ' Included Components1', ' Included Components2', ' Included Components3', ' Included Components4',
         ' Included Components5', ' Lithium Battery Energy Content', ' Additional Features1', ' Additional Features2',
         ' Additional Features3', ' Additional Features4', ' Additional Features5', ' Lithium Battery Voltage',
         ' Lithium Battery Weight', 'Occasion Type', ' Shape', ' Catalog Number', ' Finish Types', ' Specification Met',
         ' External Testing Certification', ' Matte Style', ' Fur Description', ' Fabric Type1', ' Fabric Type2',
         ' Fabric Type3', ' CPSIA Warning Description']
                            # To Form Text Dictionary Fields
        # js_text_label = response.xpath('.//*[@type="text"]/@name').extract()
        text_label_values = response.xpath('.//*[@type="text"]/@value').extract()
        text_fields = dict(zip(ui_text_label, text_label_values))

                            # To Form Image Dictionary Field
        img_values = response.xpath('.//img[@class="previewImage"]/@src').extract()[6:]
        img_names = ['main_image', 'img_1', 'img_2', 'img_3', 'img_4', 'img_5', 'img_6', 'img_7', 'img_8']
        img_dict = dict(zip(img_names, img_values))

                            # Number LAbel Names from Inspected Code
        js_num_label=['item_package_quantity', 'max_order_quantity', 'fulfillment_latency', 'number_of_sets','thread_count',
         ' Number of Batteries Required', ' Battery Type: Lithium ion', ' Battery Type: Lithium Metal',
         ' Number of Pieces', ' Number of Lithium-ion Cells', ' Number of Lithium Metal Cells',' Max Aggregate Ship Quantity']
                            # Number Label Names from UI
        ui_number_label=[' Package Quantity', ' Max Order Quantity', ' Handling Time', ' Number of Sets',
         ' Thread Countnumber_of_batteries', 'battery_type_lithium_ion', 'battery_type_lithium_metal',
         'number_of_pieces', 'number_of_lithium_ion_cells', 'number_of_lithium_metal_cells',
         'max_aggregate_ship_quantity']
                            # To Form Number Dictionary Fields
        #js_number_label = response.xpath('.//*[@type="number"]/@name').extract()
        number_label_values = response.xpath('.//*[@type="number"]/@value').extract()
        number_fields = dict(zip(ui_number_label, number_label_values))

                            #  Merging Of all Dictionary and Find Empty Fields
        text_fields.update(img_dict)
        text_fields.update(number_fields)
        emptey_fields = [i for i in text_fields.keys() if text_fields[i] is ""]



        #print(text_fields)
        #print(len(text_fields))
        #print("Emptey Fields List-------------------------------")
        #print(number_fields)
        #print(emptey_fields)
        #print(len(emptey_fields))
        ##yield {'names':ui_text_label}
        #yield (fields)
        yield {'Emptey': emptey_fields}
        #print("----------------------------------------------------------")