from django.shortcuts import render, redirect
from .models import Produto, Venda, ItensVenda, Cliente, Fornecedor, Vendedor
from .forms import ClienteForm

def home(request):
    return render(request, 'trade/home.html')

def cadastro_clientes(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClienteForm()
    return render(request, 'trade/cadastro_clientes.html', {'form': form})

def demonstrativo_tabelas(request):
    clientes = Cliente.objects.all()
    fornecedores = Fornecedor.objects.all()
    produtos = Produto.objects.all()
    vendas = Venda.objects.all()
    return render(request, 'trade/demonstrativo_tabelas.html', {
        'clientes': clientes,
        'fornecedores': fornecedores,
        'produtos': produtos,
        'vendas': vendas,
    })

def galeria_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'trade/galeria_produtos.html', {'produtos': produtos})

def realizar_venda(request):
    if request.method == 'POST':
        # Lógica simplificada para processar a venda
        cliente_id = request.POST.get('cliente')
        produto_id = request.POST.get('produto')
        quantidade = request.POST.get('quantidade')
        cliente = Cliente.objects.get(idcli=cliente_id)
        produto = Produto.objects.get(idprod=produto_id)
        vendedor = Vendedor.objects.first()  # Supondo que há um vendedor padrão
        fornecedor = produto.idforn

        valor_venda = produto.valorprod * int(quantidade)
        venda = Venda.objects.create(
            codivend='12345',  # Código de venda gerado automaticamente
            idcli=cliente,
            idforn=fornecedor,
            idvende=vendedor,
            valorvend=valor_venda,
            descvend=0,
            totalvend=valor_venda,
            datavend='2023-07-19',  # Data atual
            valorcomissao=valor_venda * vendedor.porcvende / 100
        )

        ItensVenda.objects.create(
            idvend=venda,
            idprod=produto,
            valoritvend=produto.valorprod,
            qtditvend=quantidade,
            descitvend=0
        )

        return redirect('home')

    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    return render(request, 'trade/realizar_venda.html', {
        'clientes': clientes,
        'produtos': produtos,
    })
