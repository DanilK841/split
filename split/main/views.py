from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import CostDetail, Cost, People
from .form import CostDetailForm, CostDetailFormCreate

from django.db.models import Count, Sum


# Create your views here.
class CostDetailView(DetailView):
    template_name = 'main/costdetail.html'
    model = CostDetail
    queryset = CostDetail.objects

class CostDetailCreateView(CreateView):
    model=CostDetail
    form_class = CostDetailFormCreate
    def get_success_url(self):
        return reverse('main:cost_view', kwargs={'pk': self.kwargs.get('pk')})
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Получаем параметр из URL
        kwargs['pk'] = self.kwargs.get('pk')
        print('contextcontextcontextcontext ',kwargs)
        return kwargs
    def form_valid(self, form):
        # Использование параметра при сохранении формы
        form.instance.cost = get_object_or_404(Cost, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

class CostDetailUpdateView(UpdateView):
    model = CostDetail
    template_name_suffix = '_update_form'
    form_class = CostDetailForm
    def get_success_url(self):
        return reverse('main:cost_view', kwargs={'pk': self.object.cost.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Получаем pk из URL и передаем в форму
        pk_detail = self.kwargs.get('pk')
        costdetail = get_object_or_404(CostDetail, pk=pk_detail)
        cost = get_object_or_404(Cost, pk=costdetail.cost.pk)
        kwargs['pk'] = cost.pk
        return kwargs

class CostDetailDeleteView(DeleteView):
    model=CostDetail

    def get_success_url(self):
        return reverse('main:cost_view', kwargs={'pk': self.object.cost.pk})
    # success_url = reverse_lazy('main:cost_view', kwargs={'pk':object.cost.pk})


class PeopleCreateView(CreateView):
    model=People
    fields = 'name', 'telegram'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        peoples = People.objects.filter(cost=context['pk'])
        context['peoples'] = peoples
        return context
    def get_success_url(self):
        return reverse('main:people_create', kwargs={'pk': self.kwargs.get('pk')})
    def form_valid(self, form):
        # Использование параметра при сохранении формы
        form.instance.cost = get_object_or_404(Cost, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

class PeopleCreateToCostView(CreateView):
    model=People
    fields = 'name', 'telegram'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        peoples = People.objects.filter(cost=context['pk'])
        context['peoples'] = peoples
        return context
    def get_success_url(self):
        return reverse('main:cost_view', kwargs={'pk': self.kwargs.get('pk')})
    def form_valid(self, form):
        # Использование параметра при сохранении формы
        form.instance.cost = get_object_or_404(Cost, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

class PeopleUpdateView(UpdateView):
    model = People
    fields = ('name','telegram')
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return reverse('main:cost_view', kwargs={'pk': self.object.cost.pk})

class PeopleDeleteView(DeleteView):
    model=People

    def get_success_url(self):
        return reverse('main:cost_view', kwargs={'pk': self.object.cost.pk})

class CostView(TemplateView):
    template_name = 'main/cost_detail.html'
    def evaluate_result(self, pk):
        cost_detail = CostDetail.objects.filter(cost=pk)

        people_cost = (cost_detail
        .values('people_cost__name')
        .annotate(
            total_sum_spent=Sum('price')
        ))

        res = CostDetail.objects.raw('''SELECT cd.id,
                    mp1.name as name_cost, 
                    mp2.name as name_share,
                    count(cd.id) over (partition by cd.id) as wind_,
                    cd.price,
                    cd.price / count(cd.id) over (partition by cd.id) as price_for_one
                    from main_costdetail cd
                    left join main_costdetail_people_share cds on cd.id = cds.costdetail_id
                    join main_people mp1 on cd.people_cost_id = mp1.id
                    join main_people mp2 on cds.people_id = mp2.id
                    where cd.cost_id = %s''', [str(pk).replace('-','')])
        print(f'where cd.cost_id = %s', [str(pk)])
        data = {}
        for r in res:
            print('asjkdgakjgdhjkasgdjhagsdhj', r.name_cost)
            if r.name_cost != r.name_share:
                if r.name_cost in data.keys() and r.name_share in data[r.name_cost].keys():
                    data[r.name_cost][r.name_share] += r.price_for_one
                elif r.name_cost in data.keys():
                    data[r.name_cost][r.name_share] = r.price_for_one
                else:
                    data[r.name_cost]= {r.name_share:r.price_for_one}
        print('datastart start start start', data)
        iter = 1
        while iter == 1:
            deldic = {}
            iter = 0
            for key in data.keys():
                for k, v in data[key].items():
                    if k in data.keys() and key in data[k].keys():
                        iter = 1
                        if v >= data[k][key]:
                            data[key][k] = v - data[k][key]
                            data[k][key] = 0
                            deldic[k] = key
                        else:
                            data[k][key] = data[k][key] - v
                            data[key][k] = 0
                            deldic[key] = k
            for k,v in deldic.items():
                del data[k][v]
            deldic = {}
            print(data)
            # todo add comment
            data_ = {}
            for costkey in data.keys():
                for sharekey in data[costkey].keys():
                    print(data)
                    if sharekey in data.keys() :
                        for sharekey2 in data[sharekey].keys():
                                # iter = 1
                            if data[costkey][sharekey] > 0 and data[sharekey][sharekey2] > 0:
                                if data[sharekey][sharekey2] >= data[costkey][sharekey]:
                                    if sharekey2 in data[costkey].keys():
                                        data[costkey][sharekey2] += data[costkey][sharekey]
                                    else:
                                        if costkey in data_.keys() and sharekey2 in data[costkey].keys():
                                            data_[costkey][sharekey2] += data[costkey][sharekey]
                                        elif costkey in data_.keys() :
                                            data_[costkey][sharekey2] = data[sharekey][sharekey2]
                                        else:
                                            data_[costkey] = {sharekey2: data[sharekey][sharekey2]}

                                    data[sharekey][sharekey2] -= data[costkey][sharekey]
                                    data[costkey][sharekey] = 0
                                    deldic[costkey] = sharekey
                                else:
                                    data[costkey][sharekey] -= data[sharekey][sharekey2]
                                    if sharekey2 in data[costkey].keys():
                                        data[costkey][sharekey2] += data[sharekey][sharekey2]
                                    else:
                                        if costkey in data_.keys() and sharekey2 in data[costkey].keys():
                                            data_[costkey][sharekey2] += data[sharekey][sharekey2]
                                        elif costkey in data_.keys() :
                                            data_[costkey][sharekey2] = data[sharekey][sharekey2]
                                        else:
                                            data_[costkey] = {sharekey2: data[sharekey][sharekey2]}
                                    data[sharekey][sharekey2] = 0
                                    deldic[sharekey] = sharekey2


                    # key in data[k].keys():

            for k,v in deldic.items():
                del data[k][v]
            deldic = {}
            print('data_:', data_)
            for costkey in data_.keys():
                for sharekey in data_[costkey].keys():
                    data[costkey][sharekey] = data_[costkey][sharekey]
            data_ = {}
            print('data:', data)

        data_n = {}
        for costkey in data.keys():
            for sharekey in data[costkey].keys():
                if sharekey in data_n.keys():
                    data_n[sharekey][costkey] = data[costkey][sharekey]
                else:
                    data_n[sharekey] = {costkey: data[costkey][sharekey]}
        print(data_n)
        return  {'people_cost':people_cost,
                 'res':res,
                 'data':data_n,
                 }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cost = get_object_or_404(Cost, pk=context['pk'])
        peoples = People.objects.filter(cost=context['pk'])
        context['peoples'] = peoples
        context['cost'] = cost
        context['result'] = self.evaluate_result(context['pk'])
        return context

class CostCreateView(CreateView):
    model=Cost
    fields = ('name',)
    def get_success_url(self):
        print('print args', self.kwargs)
        return reverse_lazy('main:people_create', kwargs={'pk': self.object.pk})
