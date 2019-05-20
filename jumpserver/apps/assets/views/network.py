from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from common.permissions import AdminUserRequiredMixin
from ..models import NetworkDevice, Node, IdcNode


class NetworkListView(AdminUserRequiredMixin, TemplateView):

    template_name = 'assets/network_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '网络设备',
            'nodes': Node.objects.all().order_by('date_create')[1:],
            'lables': NetworkDevice.objects.all().order_by('-m_time'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


@login_required(login_url='/users/login/')
def networknodelist(request,nodename):
    if request.user.is_superuser:
        app = '网络设备'
        nodes =  Node.objects.all().order_by('date_create')[1:]
        node =  Node.objects.get(value=nodename)
        lables =  NetworkDevice.objects.filter(node=node.id).order_by('m_time')
        return render(request, 'assets/node_list.html', {'nodes':nodes,'lables':lables,'app':app})
    else:
        return redirect('/')


@login_required(login_url='/users/login/')
def networkdrivecreate(request):
    if request.user.is_superuser:
        nodes = Node.objects.all().order_by('date_create')[1:]
        if request.method == 'POST':
            print(request.POST)
            try:
                obj = NetworkDevice()
                obj.net_name = request.POST['name'].strip()
                obj.sub_asset_type = request.POST['type'].strip()
                obj.ip1 = request.POST['IP1'].strip()
                obj.ip2 = request.POST['IP2'].strip()
                obj.port_num = request.POST['port_num'].strip()
                obj.device_detail = request.POST['config'].strip()
                obj.message = request.POST['comment'].strip()
                obj.save()

                for nod in request.POST.getlist('nodes'):
                    # if  nod != 'default':
                    node = Node.objects.get(value=nod)
                    obj.node.add(node)
                return redirect('/assets/network/')
            except Exception as e:
                print(e)
                message = "参数错误"
                return render(request, 'assets/network_create.html', {'nodes': nodes,'message': message})
        return render(request, 'assets/network_create.html', {'nodes': nodes})
    else:
        return redirect('/')


@login_required(login_url='/users/login/')
def nodeview(request):
    if request.user.is_superuser:
        # nodes = Node.objects.all().order_by('date_create')[1:]
        # for i in nodes:
        #     print(i.IdcNode)
        nodes = IdcNode.objects.all()

        return render(request, 'assets/network_node_list.html', {'nodes': nodes})
    else:
        return redirect('/')


@login_required(login_url='/users/login/')
def createnode(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            print(request.POST)
            try:
                node = Node.root()
                node.create_child(value=request.POST['name'].strip())
                node = Node.objects.get(value=request.POST['name'].strip())
                obj = IdcNode()
                obj.addr = request.POST['addr'].strip()
                obj.tel = request.POST['tel'].strip()
                obj.user = request.POST['user'].strip()
                obj.node_name = node
                obj.message = request.POST['comment'].strip()
                obj.save()
                return redirect('/assets/nodeview/nodeview/')
            except Exception as e:
                print(e)
                message = "参数错误"
                return render(request, 'assets/node_create.html', {'message': message})
        return render(request,'assets/node_create.html')
    else:
        return redirect('/')


@login_required(login_url='/users/login/')
def updatenetwork(request, n_id):
    if request.user.is_superuser:
        if request.method == 'GET':
            nodes = Node.objects.all().order_by('date_create')[1:]
            lable = NetworkDevice.objects.get(pk=n_id)
            lable_node = lable.node.all()
            if lable_node:
                print('有节点')
                return render(request, 'assets/update_network.html',
                              {'nodes': nodes, 'lable': lable, 'lable_node': lable_node})
            else:
                lable_node = 'default'
                print('没有节点',lable_node)
                return render(request,'assets/update_network.html',
                              {'nodes':nodes,'lable':lable,'lable_node':lable_node})

        if request.method == 'POST':

            nodes = Node.objects.all().order_by('date_create')[1:]
            lable = NetworkDevice.objects.get(pk=n_id)
            lable_node = lable.node.all()
            try:
                obj = NetworkDevice.objects.get(pk=n_id)
                obj.net_name = request.POST['name'].strip()
                obj.sub_asset_type = request.POST['type'].strip()
                obj.ip1 = request.POST['IP1'].strip()
                obj.ip2 = request.POST['IP2'].strip()
                obj.port_num = request.POST['port_num'].strip()
                obj.device_detail = request.POST['config'].strip()
                obj.message = request.POST['comment'].strip()
                obj.save()

                for i in lable_node:
                    obj.node.remove(i)

                for nod in request.POST.getlist('nodes'):
                    #if nod != 'default':
                    try:
                        node =Node.objects.get(value=nod)
                        obj.node.add(node)
                    except Exception as e:
                        print(e)
                        node = Node.objects.get(value=nod)
                        obj.node.add(node)
                    # if nod == 'default':
                    #     pass
                return redirect('/assets/network/')
            except Exception as e:
                print(e)
                message = "参数错误"
                return render(request, 'assets/update_network.html',
                              {'nodes': nodes, 'lable': lable, 'lable_node': lable_node, 'message':message})
    else:
        return redirect('/')


@login_required(login_url='/users/login/')
def updatenode(request, n_id):
    if request.user.is_superuser:
        node = IdcNode.objects.get(pk=n_id)
        if request.method == 'POST':
            node.node_name.value = request.POST['name'].strip()
            node.addr = request.POST['addr'].strip()
            node.tel = request.POST['tel'].strip()
            node.user = request.POST['user'].strip()
            node.message = request.POST['comment'].strip()
            node.save()
            return redirect('/assets/nodeview/nodeview/')
        return render(request,'assets/update_node.html',{'node': node})
    else:
        return redirect('/')


@login_required(login_url='/users/login/')
def networkdetail(request,n_id):
    lable = NetworkDevice.objects.get(pk=n_id)
    lable_node = lable.node.all()
    return render(request,'assets/network_detail.html',{'lable':lable,'lable_node':lable_node})


@login_required(login_url='/users/login/')
def networkdel(request,n_id):
    if request.user.is_superuser:
        NetworkDevice.objects.filter(pk=n_id).delete()
        return redirect("/assets/network/")
    else:
        return redirect('/')


@login_required(login_url='/users/login/')
def nodedel(request, n_id):
    if request.user.is_superuser:
        obj = IdcNode.objects.get(pk=n_id)
        Node.objects.filter(pk=obj.node_name.id).delete()
        return redirect("/assets/nodeview/nodeview/")
    else:
        return redirect('/')



class UserNetworkList(LoginRequiredMixin, TemplateView):

    template_name = 'assets/user_network_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '网络设备',
            'nodes': Node.objects.all().order_by('date_create')[1:],
            'lables': NetworkDevice.objects.all().order_by('-m_time'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


@login_required(login_url='/users/login/')
def usernetworknodelist(request, nodename):
    app = '网络设备'
    nodes = Node.objects.all().order_by('date_create')[1:]
    node = Node.objects.get(value=nodename)
    lables = NetworkDevice.objects.filter(node=node.id).order_by('m_time')
    return render(request, 'assets/user_node_list.html', {'nodes': nodes, 'lables': lables, 'app': app})
