from django.shortcuts import render, redirect, get_object_or_404
from Style_Information_app.models import Customer, StyleInfo, StyleDescription
from collections import defaultdict
def style_info_add(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer_name", "").upper()
        style_no = request.POST.get("style_no", "").upper()
        season = request.POST.get("season", "").upper()
        production_line = request.POST.get("production_line", "").upper()
        order_qty = request.POST.get("order_qty", 0)
        apm = request.POST.get("apm", "").capitalize()
        technician = request.POST.get("technician", "").capitalize()
        qc = request.POST.get("qc", "").capitalize()
        qa = request.POST.get("qa", "").capitalize()
        tqs = request.POST.get("tqs", "").capitalize()

        customer, _ = Customer.objects.get_or_create(customer_name=customer_name)
        style = StyleInfo.objects.create(
            customer=customer,
            style_no=style_no,
            season=season,
            production_line=production_line,
            order_qty=order_qty,
            apm=apm,
            technician=technician,
            qc=qc,
            qa=qa,
            tqs=tqs
        )

        if request.POST.get("style_description"):  
            StyleDescription.objects.create(
                style=style,
                style_description=request.POST.get("style_description")
            )

        return redirect('add_style_overview')

    return render(request, 'style_information/style_info_add.html')

def add_style_overview(request):
    styles = StyleInfo.objects.prefetch_related("descriptions").all()

    grouped = defaultdict(lambda: {"rows": [], "descriptions": {}})  

    for s in styles:
        key = (s.customer.customer_name, s.style_no)
        row_key = (
            s.season,
            s.production_line,
            s.apm,
            s.technician,
            s.qc,
            s.qa,
            s.tqs,
        )

        if row_key not in [(
            r.season,
            r.production_line,
            r.apm,
            r.technician,
            r.qc,
            r.qa,
            r.tqs
        ) 

        for r in grouped[key]["rows"]]:
            grouped[key]["rows"].append(s)

        for d in s.descriptions.all():
            if d.style_description not in grouped[key]["descriptions"]:
                grouped[key]["descriptions"][d.style_description] = d

    merged_styles = []
    for (customer, style_no), data in grouped.items():
        merged_styles.append({
            "customer": customer,
            "style_no": style_no,
            "rows": data["rows"],
            "descriptions": list(data["descriptions"].values()),  # distinct objects
            "rowspan": len(data["rows"]),
        })

    return render(request, "style_information/add_style_overview.html", {
        "styles": merged_styles
    })

# Delete StyleInfo
def delete_add_style_overview(request, id):
    style = get_object_or_404(StyleInfo, id=id)
    style.delete()
    return redirect('add_style_overview')

# after click the style description show this page
def style_detail(request, style_id):
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
        'style': styles,
        'style_id': style_id,
    }
    return render(request, 'style_information/style_detail.html', context)

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