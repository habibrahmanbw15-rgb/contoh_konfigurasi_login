import re

class Template():
    def __init__(self, text):
        self.delimiter = re.compile(r'\{%(.*?)%\}', re.DOTALL)
        self.tokens = self.compile(text)
    def compile(self, text):
        tokens = []
        for index, token in enumerate(self.delimiter.split(text)):
            if index % 2 == 0:
                if token:
                    tokens.append((False, token.replace('\\%',
                    '%').replace('{\\%', '{%').replace('%\\}', '%}')))
            else:
                lines = token.replace('\\%', '%').replace('{\\%',
                '%').replace('%\\}', '%}').splitlines()
                indent = min([len(l) - len(l.lstrip()) for l in lines if
                l.strip()])
                realigned = '\n'.join([l[indent:] for l in lines])
                tokens.append((True, compile(realigned, '<template> %s' %
                realigned[:20], 'exec')))
        return tokens
    def render(self, context = None, **kw):
        global_context = {}
        if context:
            global_context.update(context)
        if kw:
            global_context.update(kw)
        def emit(*args):
            result.extend([str(arg) for arg in args])
        def fmt_emit(fmt, *args):
            result.append(fmt % args)
        global_context['emit'] = emit
        global_context['fmt_emit'] = fmt_emit
        result = []
        for is_code, token in self.tokens:
            if is_code:
                exec(token, global_context)
            else:
                result.append(token)
        return ''.join(result)