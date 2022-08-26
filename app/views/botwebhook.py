from django.http import HttpResponse
from telegram import Update
from bots.applicant.update import dp as applicant_dp, updater as applicant_updater
from bots.supplier.update import dp as supplier_dp, updater as supplier_updater
import json
from django.views.decorators.csrf import csrf_exempt
from config import DEBUG


@csrf_exempt
def applicant_webhook(request):

    if DEBUG:
        # applicant_dp.update_persistence()
        applicant_updater.start_polling()
    else:
        update = Update.de_json(json.loads(request.body.decode("utf-8")), applicant_dp.bot)
        applicant_dp.run_async(applicant_dp.update_persistence(update))
        applicant_dp.run_async(applicant_dp.process_update(update))
        # applicant_dp.process_update(update)
        # applicant_dp.start()
    return HttpResponse("Bot started!")



@csrf_exempt
def supplier_webhook(request):
    if DEBUG:
        # supplier_dp.update_persistence()
        supplier_updater.start_polling()
    else:
        update = Update.de_json(json.loads(request.body.decode("utf-8")), supplier_dp.bot)
        # supplier_dp.run_async(supplier_dp.process_update(update))
        supplier_dp.update_persistence(update)
        supplier_dp.process_update(update)
        # supplier_dp.start()
    return HttpResponse("Bot started!")
