from django.shortcuts import render, redirect, get_object_or_404
from Style_Information_app.models import Customer, StyleInfo

# Add Style Info Page
def style_info_add(request):
    if request.method == "POST":
        # Get form data
        customer_name = request.POST.get("customer_name", "").upper()
        season = request.POST.get("season", "").upper()
        style_no = request.POST.get("style_no", "").upper()
        production_line = request.POST.get("production_line", "").upper()
        order_qty = request.POST.get("order_qty", 0)
        apm = request.POST.get("apm", "").capitalize()
        technician = request.POST.get("technician", "").capitalize()
        qc = request.POST.get("qc", "").capitalize()
        qa = request.POST.get("qa", "").capitalize()
        tqs = request.POST.get("tqs", "").capitalize()

        customer, _ = Customer.objects.get_or_create(customer_name=customer_name)
        StyleInfo.objects.create(
            customer=customer,
            season=season,
            style_no=style_no,
            production_line=production_line,
            order_qty=order_qty,
            apm=apm,
            technician=technician,
            qc=qc,
            qa=qa,
            tqs=tqs
        )
        return redirect('add_style_overview')
    return render(request, 'style_information/style_info_add.html')

def add_style_overview(request):
    styles = StyleInfo.objects.all()
    return render(request, 'style_information/add_style_overview.html', {'styles': styles})


# Delete StyleInfo
def delete_add_style_overview(request, id):
    style = get_object_or_404(StyleInfo, id=id)
    style.delete()
    return redirect('add_style_overview')


def style_summary(request):
    styles = StyleInfo.objects.all()   # ✅ full model name

    # Extract unique values for dropdowns
    customers = styles.values_list("customer__customer_name", flat=True).distinct()
    seasons = styles.values_list("season", flat=True).distinct()
    lines = styles.values_list("production_line", flat=True).distinct()
    apms = styles.values_list("apm", flat=True).distinct()
    technicians = styles.values_list("technician", flat=True).distinct()
    qcs = styles.values_list("qc", flat=True).distinct()
    qas = styles.values_list("qa", flat=True).distinct()
    tqss = styles.values_list("tqs", flat=True).distinct()
    style_nos = styles.values_list("style_no", flat=True).distinct()

    context = {
        "customers": customers,
        "seasons": seasons,
        "lines": lines,
        "apms": apms,
        "technicians": technicians,
        "qcs": qcs,
        "qas": qas,
        "tqss": tqss,
        "style_nos": style_nos,
    }
    return render(request, 'style_information/style_info_summary.html', context)

def add_comments(request):
    return render(request, 'style_information/add_comments.html')