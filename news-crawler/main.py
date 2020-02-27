from usp.tree import sitemap_tree_for_homepage

tree = sitemap_tree_for_homepage('https://www.nytimes.com/')
for page in tree.all_pages():
    print(page)