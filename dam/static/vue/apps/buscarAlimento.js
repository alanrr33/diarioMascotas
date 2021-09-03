new Vue({
    el:'#app',
    delimiters: ['{$', '$}'],

    created()
     {
       let url = window.location.href;
           //console.log(urlParams.has('74')); // true
           //console.log(urlParams.get('74')); // "MyParam"
            console.log(url);
            diario_id=(url.split("/")[5]);
            console.log('diario_id= '+diario_id)
         
     },

    data:{
        kword:'',
        diario_id:'',
        lista_alimentos_agregados:[],
        lista_resultados:[],
    },

    

    watch:{
        kword:function(val){
            this.buscarAlimentos(val);
        }
    },

    methods: {
        buscarAlimentos: function(kword){
            var self=this;
            axios.get('/alimentos/api/alimentos/buscar/?kword='+kword)
                .then(function(response){
                    self.lista_resultados=response.data
                    
                })
                .catch(function(error){
                    console.log(error);
                });
            
        },

        agregarAlimento:function(){
            ///this.lista_alimentos_agregados.push(alimento)
            console.log(this.lista_alimentos_agregados)
        }



        
    },


});