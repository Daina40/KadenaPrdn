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

    # First group by customer
    customer_grouped = defaultdict(lambda: {"styles": {}, "rowspan": 0})

    for s in styles:
        cust = s.customer.customer_name
        style_no = s.style_no

        # group by style inside each customer
        if style_no not in customer_grouped[cust]["styles"]:
            customer_grouped[cust]["styles"][style_no] = {
                "rows": [],
                "descriptions": {},
            }

        # deduplicate rows
        row_key = (
            s.season,
            s.production_line,
            s.apm,
            s.technician,
            s.qc,
            s.qa,
            s.tqs,
        )
        if row_key not in [
            (
                r.season,
                r.production_line,
                r.apm,
                r.technician,
                r.qc,
                r.qa,
                r.tqs,
            )
            for r in customer_grouped[cust]["styles"][style_no]["rows"]
        ]:
            customer_grouped[cust]["styles"][style_no]["rows"].append(s)
            customer_grouped[cust]["rowspan"] += 1  # increase total rowspan for customer

        # collect distinct descriptions
        for d in s.descriptions.all():
            if d.style_description not in customer_grouped[cust]["styles"][style_no]["descriptions"]:
                customer_grouped[cust]["styles"][style_no]["descriptions"][d.style_description] = d

    # Prepare for template
    merged_customers = []
    for customer, cdata in customer_grouped.items():
        styles_list = []
        for style_no, sdata in cdata["styles"].items():
            styles_list.append({
                "style_no": style_no,
                "rows": sdata["rows"],
                "descriptions": list(sdata["descriptions"].values()),
                "rowspan": len(sdata["rows"]),
            })
        merged_customers.append({
            "customer": customer,
            "styles": styles_list,
            "rowspan": cdata["rowspan"],
        })

    return render(request, "style_information/add_style_overview.html", {
        "customers": merged_customers
    })

# Delete StyleInfo
def delete_add_style_overview(request, id):
    style = get_object_or_404(StyleInfo, id=id)
    style.delete()
    return redirect('add_style_overview')

def style_detail(request, style_id):
    style = get_object_or_404(StyleInfo, id=style_id)
    
    description = style.descriptions.first()
    
    # All distinct values for filters or dropdowns
    styles = StyleInfo.objects.all()
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
        "style": style,
        "description": description,
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
    return render(request, "style_information/style_detail.html", context)


def style_saved_table(request, saved_id=None):
    styles = StyleInfo.objects.prefetch_related("descriptions", "customer").all()

    if saved_id:
        styles = styles.filter(id=saved_id)

    # Group by customer → then by style
    customer_grouped = defaultdict(lambda: {"styles": {}, "rowspan": 0})

    for s in styles:
        cust_name = s.customer.customer_name
        style_no = s.style_no

        # Attach first description to the StyleInfo instance
        s.first_description = s.descriptions.first()

        if style_no not in customer_grouped[cust_name]["styles"]:
            customer_grouped[cust_name]["styles"][style_no] = {
                "rows": [],
            }

        # Add the row
        customer_grouped[cust_name]["styles"][style_no]["rows"].append(s)
        customer_grouped[cust_name]["rowspan"] += 1

    # Prepare data for template
    merged_customers = []
    for customer, cdata in customer_grouped.items():
        styles_list = []
        for style_no, sdata in cdata["styles"].items():
            styles_list.append({
                "style_no": style_no,
                "rows": sdata["rows"],
                "rowspan": len(sdata["rows"]),
            })
        merged_customers.append({
            "customer": customer,
            "styles": styles_list,
            "rowspan": cdata["rowspan"],
        })

    return render(request, "style_information/style_saved_table.html", {
        "customers": merged_customers
    })


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