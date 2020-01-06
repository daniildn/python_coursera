use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product

-- 2. Выбрать названия всех автоматизированных складов
select store.name from store;

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(sale.total) from sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select distinct store.store_id from store natural join sale ;

-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select distinct store.store_id from store left join sale using(store_id) where sale_id IS NULL;

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select product.name, avg(total/quantity) from sale natural join product group by product.name;

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select  name as name from product
natural join sale
group by name
having count(distinct store_id) = 2;

-- 8. Получить названия всех складов, с которых продавался только один продукт
select name from store
natural join sale
group by name
having count(distinct product_id) = 1;

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from sale
order by total desc
    limit 1;
-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date from sale
group by date
order by sum(quantity)desc limit 1;
