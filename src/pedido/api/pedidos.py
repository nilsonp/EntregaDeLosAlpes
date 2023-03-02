import pedido.seedwork.presentacion.api as api
import json
from pedido.seedwork.dominio.excepciones import ExcepcionDominio
from pedido.seedwork.aplicacion.queries import ejecutar_query
from flask import Response, request
from pedido.modulos.pedidos.aplicacion.mapeadores import MapeadorPedidoDTOJson
from pedido.modulos.pedidos.aplicacion.comandos.crear_pedido import CrearPedido
from pedido.modulos.pedidos.aplicacion.queries.obtener_pedido import ObtenerPedido

bp = api.crear_blueprint('pedidos', '/pedidos')

@bp.route('/pedido-comando', methods=('POST',))
def reservar_asincrona():

    try:
        pedido_dict = request.json

        map_pedido = MapeadorPedidoDTOJson()
        pedido_dto = map_pedido.externo_a_dto(pedido_dict) 

        comando = CrearPedido(id=pedido_dto.id, fecha_actualizacion=pedido_dto.fecha_actualizacion, fecha_creacion=pedido_dto.fecha_creacion)
        #ejecutar_comando(comando)

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@bp.route('/<id>', methods=('GET',))
def get_pedido(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerPedido(id))
        map_pedido = MapeadorPedidoDTOJson()
        return map_pedido.dto_a_externo(query_resultado.resultado)
    else: 
        return [{'message': 'GET!'}]
