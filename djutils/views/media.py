# -*- coding: utf-8 -*-
import re
import os.path
from subprocess import Popen, PIPE
from tempfile import TemporaryDirectory

from django.http import HttpResponse
from django.template.loader import select_template
from django.views.generic import TemplateView


class PdfLatexView(TemplateView):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        template = select_template(self.get_template_names())
        latex_content = template.render(context)
        latex_content = re.sub(r'\{ ', '{', latex_content)
        latex_content = re.sub(r' \}', '}', latex_content)
        pdf_content = None
        with TemporaryDirectory() as tempdir:
            """Create subprocess, suppress output iwth PIPE and runs latex
            twice to generate correct the TOC and pagination propertly.
            """
            for i in range(2):
                process = Popen(
                    ['xelatex', '-output-directory', tempdir],
                    stdin=PIPE, stdout=PIPE)
                process.communicate(latex_content.encode('utf-8'))
            with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
                pdf_content = f.read()
        response = HttpResponse(content_type='application/pdf')
        response.write(pdf_content)
        return response
