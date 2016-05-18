# -*- coding: utf-8 -*
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.utils import safe_unicode
#from zope.component import getMultiAdapter

#from zope.event import notify
#from zope.lifecycleevent import ObjectModifiedEvent
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

from plone import api
import logging


class BayesFilter(BrowserView):
    """ Bayes Filter
    """

    def __call__(self, text):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog

        bayesFilter = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.bayesFilter')

        trainingSet = []
        for line in bayesFilter.split('\n'):
            trainingSet.append({'category':'hasKey', 'text':safe_unicode(line)})

        trainer = Trainer(tokenizer)
        for record in trainingSet:
            trainer.train(record['text'], record['category'])
        classifier = Classifier(trainer.data, tokenizer)

        result = classifier.classify(safe_unicode(text))

        import pdb; pdb.set_trace()
