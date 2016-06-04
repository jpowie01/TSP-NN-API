from flask import request, make_response
from flask.ext.restplus import Resource
from pybrain.tools.customxml import NetworkReader

from api import api, app, tsp
from serializers import tsp_model_input, tsp_model_output
from graph import Graph, convert_output


N = 6
net = NetworkReader.readFrom('neural_network.xml')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@tsp.route('/')
class TodoList(Resource):

    @api.expect(tsp_model_input)
    @api.marshal_with(tsp_model_output, code=200)
    def post(self):
        # Get data
        graph_json = request.get_json(force=True)

        # Create graph
        graph = Graph(N)
        graph.graph = []
        graph_points = graph_json.get('graph')
        for point in sorted(graph_points, key=lambda graph_point: graph_point.get('id')):
            graph.graph.append((point['x'], point['y']))
        graph.compute_each_to_each()
        graph.compute_tsp()

        # Prepare input for neural network
        input = ()
        for j in range(N):
            for k in range(N):
                input += (graph.each_to_each[j][k],)

        # Calculate proper output
        output = [[] for x in range(N)]
        for j in range(N):
            output[j] = [[] for y in range(N)]
        for j in range(N):
            for k in range(N):
                if graph.order_tsp[j] == k:
                    output[k][j] = 1
                else:
                    output[k][j] = 0

        # Calculate neural network output
        net_output = net.activate(input)
        net_output_array = [[] for x in range(N)]
        for j in range(N):
            net_output_array[j] = [[] for y in range(N)]
        for j in range(N):
            for k in range(N):
                net_output_array[k][j] = net_output[j * N + k]

        # Calculate order
        order = convert_output(net_output, N)

        # Original
        original_len = 0
        for j in range(N - 1):
            original_len += graph.each_to_each[graph.order_tsp_list[j]][graph.order_tsp_list[j + 1]]
        original_len += graph.each_to_each[graph.order_tsp_list[N - 1]][graph.order_tsp_list[0]]

        # Compute
        network_len = 0
        for j in range(N - 1):
            network_len += graph.each_to_each[order[j]][order[j + 1]]
        network_len += graph.each_to_each[order[N - 1]][order[0]]

        # Log
        print('Original:', original_len, 'Network:', network_len, 'Error:', abs(original_len-network_len)/original_len*100, '%')

        # Update order
        graph.order_tsp_list = list(map(lambda x: x + 1, graph.order_tsp_list))
        order = list(map(lambda x: x + 1, order))

        # Send response
        return {
            'expected': output,
            'net': net_output_array,
            'expected_order': graph.order_tsp_list,
            'net_order': order,
            'net_error': abs(original_len-network_len)/original_len * 100
        }


if __name__ == '__main__':
    app.run(host='localhost', debug=False)
