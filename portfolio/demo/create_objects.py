# coding: utf-8

import sys
import os
import argparse


CATEGORY_SITE_IMAGE = 'upload_category/demo/image.jpg'
PRODUCT_IMAGE = 'upload_product/demo/image.jpg'


def args():
    parser = argparse.ArgumentParser(description='Generate test '
                                                 'objects for catalog demo')
    # parser.add_argument('PROJECT_PATH', nargs='+', help='PROJECT_PATH help')
    return parser.parse_args()


def main(project_dir):
    project_dir = project_dir or os.getcwd().split('apps')[0]
    sys.path.append(project_dir)
    sys.path.append(os.path.join(project_dir, u'apps'))
    os.environ[u'DJANGO_SETTINGS_MODULE'] = u'settings'

    import django
    django.setup()

    from mixer.backend.django import mixer, Mixer
    from portfolio.models import Category, Portfolio, PortfolioAttachment

    # Generate a random category site
    mixer = Mixer(commit=False)
    category_site_s = mixer.cycle(5).blend(Category)
    for cat_site in category_site_s:
        print(cat_site.slug_title)
        cat_site_obj = Category.add_root(
            title=cat_site.title,
            slug_title=cat_site.slug_title,
            preview=cat_site.preview,
            content=cat_site.content,
            show=cat_site.show,
            image=CATEGORY_SITE_IMAGE,
            position=cat_site.position
        )
        cat_site_obj.save()

    # Generate a random portfolio
    mixer = Mixer(commit=True)
    portfolio_s = mixer.cycle(50).blend(Portfolio,
                                        image=PRODUCT_IMAGE,
                                        category=(cat for cat in
                                                    list(Category.objects.all())*100),
                                        import_fl=1)

    # Generate a random product attachment
    portfolio_attachment_s = mixer.cycle(100).blend(PortfolioAttachment,
                                                    portfolio=(portfolio for portfolio in
                                                               list(Portfolio.objects.all())*2),
                                                    file=PRODUCT_IMAGE,
                                                    image=PRODUCT_IMAGE
                                                    )
    print(Portfolio.objects.all())


if __name__ == '__main__':
    args = args()
    main(None)
