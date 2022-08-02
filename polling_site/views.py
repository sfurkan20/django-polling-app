import math
from django.views.generic import ListView
from polls.models import PollModel

class IndexView(ListView):
    paginate_by = 4
    template_name = "index.html"

    def get_queryset(self):
        polls = list(PollModel.objects.filter(isPublic=True))

        totalItems = 0
        pollsRows = []
        for rowIndex in range(math.ceil(len(polls) / 4)):
            pollsOfRow = []
            for columnIndex in range(min(4, len(polls) - totalItems)):
                poll = polls[(rowIndex * 4) + columnIndex]
                pollsOfRow.append(poll)

                totalItems += 1
            pollsRows.append(pollsOfRow)
        
        return pollsRows