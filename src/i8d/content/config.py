from i8d.content import _
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


ORDER_STATE = SimpleVocabulary(
    [SimpleTerm(value=u'ordered', title=_(u'ordered')),
     SimpleTerm(value=u'paid', title=_(u'paid')),
     SimpleTerm(value=u'shipped', title=_(u'shipped')),
     SimpleTerm(value=u'arrived', title=_(u'arrived')),
     SimpleTerm(value=u'inreturn', title=_(u'inreturn')),
     SimpleTerm(value=u'returned', title=_(u'returned')),
     SimpleTerm(value=u'overdue', title=_(u'overdue')),]
    )

