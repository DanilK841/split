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
    def get_success_url(self):
        return reverse('main:cost_detail_create', kwargs={'pk': self.kwargs.get('pk')})
    def form_valid(self, form):
        # Использование параметра при сохранении формы
        form.instance.cost = get_object_or_404(Cost, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

class PeopleCreateToCostView(CreateView):
    model=People
    fields = 'name', 'telegram'
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
        res = cost_detail.prefetch_related('people_share').values('people_cost','people_share').annotate(
            count=Count('id'),
            total_sum_spent=Sum('price'),
            spent_for_one=(Sum('price')/Count('id')),

        )
        print(res)
        data = {}
        # for item in res:
        #     data_ = {item.people_cost.id: {}}
        #     for itemk in item.people_share.all().values('id'):
        #         # Добавляем во вложенный словарь
        #         if itemk['id'] != item.people_cost.id:
        #             data_[item.people_cost.id][itemk['id']] = item.spent_for_one
        #
        #             # print(data_)
        #             data |= data_


        datatest = {1:{2:200, 3:200}}

        return  {'people_cost':people_cost,
                 'res':res,
                 # 'data':data,
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
        return reverse_lazy('main:people_create', kwargs={'pk': self.kwargs.get('pk')})
