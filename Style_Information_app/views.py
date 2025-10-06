import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from Style_Information_app.models import Customer, StyleInfo, StyleDescription,Comment
from collections import defaultdict
from django.utils import timezone
from django.contrib import messages

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
            tqs=tqs,
            source='overview' 
        )

        if request.POST.get("style_description"):  
            StyleDescription.objects.create(
                style=style,
                style_description=request.POST.get("style_description")
            )

        return redirect('add_style_overview')

    return render(request, 'style_information/style_info_add.html')

from django.db.models import Prefetch, Q

def add_style_overview(request):
    # Fetch overview styles for rows
    overview_styles = StyleInfo.objects.filter(source='overview').prefetch_related("descriptions", "customer").all()

    # Fetch all detail styles (just for merging their descriptions)
    detail_styles = StyleInfo.objects.filter(source='detail').prefetch_related("descriptions")

    # Map: style_no -> set of descriptions from detail records
    detail_desc_map = defaultdict(set)
    for d in detail_styles:
        for desc in d.descriptions.all():
            detail_desc_map[d.style_no].add(desc)

    # Group overview data
    customer_grouped = defaultdict(lambda: {"styles": {}, "rowspan": 0})

    for s in overview_styles:
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
            customer_grouped[cust]["rowspan"] += 1

        # ✅ Collect distinct descriptions from overview and detail
        combined_descs = list(s.descriptions.all()) + list(detail_desc_map.get(style_no, []))
        for d in combined_descs:
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
    
    comments_dict = {
        c.process: c.comment_text
        for c in style.comments.all()
    }
    
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
        "comments_dict": comments_dict,
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

def save_comments(request, style_id):
    style = get_object_or_404(StyleInfo, id=style_id)

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            process = data.get("process")
            comment_text = data.get("comment")

            if not process or not comment_text:
                return JsonResponse({"success": False, "error": "Invalid input."}, status=400)

            # Save or update comment
            comment_obj, created = Comment.objects.update_or_create(
                style=style,
                process=process,
                defaults={"comment_text": comment_text}
            )

            return JsonResponse({
                "success": True,
                "process": process,
                "comment": comment_text,
                "created": created
            })

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON."}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)
def save_style_info(request, style_id):
    original_style = get_object_or_404(StyleInfo, id=style_id)

    if request.method == "POST":
        # Create a new StyleInfo for "detail"
        new_style = StyleInfo.objects.create(
            customer=original_style.customer,
            style_no=original_style.style_no,
            source='detail',
            season=request.POST.get("season"),
            production_line=request.POST.get("production_line"),
            apm=request.POST.get("apm"),
            technician=request.POST.get("technician"),
            qc=request.POST.get("qc"),
            qa=request.POST.get("qa"),
            tqs=request.POST.get("tqs"),
            program=request.POST.get("program"),
        )

        order_qty = request.POST.get("order_qty")

        if not order_qty or not order_qty.isdigit() or int(order_qty) <= 0:
            messages.error(request, "Order quantity is required and must be a positive number.")
            return redirect("style_detail", style_id=style_id)

        new_style.order_qty = int(order_qty)
        new_style.save()

        new_style.descriptions.add(*original_style.descriptions.all())


        messages.success(request, "Style information saved successfully.")
        return redirect("style_saved_table")

    return redirect("style_detail", style_id=style_id)


def style_saved_table(request):
    styles = StyleInfo.objects.filter(source='detail').prefetch_related("descriptions", "customer").order_by('-created_at')
    
    # Grouping logic stays the same
    customer_grouped = defaultdict(lambda: {"styles": {}, "rowspan": 0})

    for s in styles:
        cust_name = s.customer.customer_name
        style_no = s.style_no
        s.first_description = s.descriptions.first()

        if style_no not in customer_grouped[cust_name]["styles"]:
            customer_grouped[cust_name]["styles"][style_no] = {"rows": []}

        customer_grouped[cust_name]["styles"][style_no]["rows"].append(s)
        customer_grouped[cust_name]["rowspan"] += 1

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